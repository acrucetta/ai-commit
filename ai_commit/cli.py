#!/usr/bin/env python3
import subprocess
import click
import anthropic
import os
from pathlib import Path
from .constants import SYSTEM_PROMPT
import json
import re

def get_api_key() -> str:
    """Get API key from environment or config file."""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key:
        return api_key
        
    config_file = Path.home() / '.config' / 'commit-msg-gen' / 'config.json'
    if config_file.exists():
        try:
            return json.loads(config_file.read_text()).get('api_key')
        except Exception:
            pass
    return None

def save_api_key(api_key: str):
    """Save API key to config file."""
    config_dir = Path.home() / '.config' / 'commit-msg-gen'
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / 'config.json'
    config_file.write_text(json.dumps({'api_key': api_key}))

def get_staged_changes() -> str:
    """Get the staged changes from git."""
    try:
        return subprocess.check_output(
            ['git', 'diff', '--cached', '--unified=1'],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
    except subprocess.CalledProcessError as e:
        raise click.ClickException(f"Error getting git diff: {e.output}")

def extract_commit_message(response: str) -> str:
    """Extract commit message from between XML tags."""
    pattern = r'<commit_message>(.*?)</commit_message>'
    match = re.search(pattern, response, re.DOTALL)
    if not match:
        raise click.ClickException("Failed to parse commit message from response")
    
    # Clean up the message
    message = match.group(1).strip()
    
    return message.strip()

def generate_commit_message(client: anthropic.Client, diff: str) -> str:
    """Generate a conventional commit message using Claude API."""
    formatted_prompt = SYSTEM_PROMPT.replace("{{STAGED_CHANGES}}", diff)
    
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0,
            messages=[{
                "role": "user",
                "content": formatted_prompt
            }]
        )
        
        commit_message = extract_commit_message(response.content[0].text)
        if not commit_message:
            raise click.ClickException("Generated commit message is empty")
            
        return commit_message
        
    except anthropic.APIError as e:
        raise click.ClickException(f"API error: {str(e)}")
    except Exception as e:
        raise click.ClickException(f"Error generating commit message: {str(e)}")

@click.group()
def cli():
    """AI-powered conventional commit message generator."""
    pass

@cli.command()
@click.option('--api-key', help='Anthropic API key')
def configure(api_key):
    """Configure the commit message generator."""
    if not api_key:
        api_key = click.prompt('Please enter your Anthropic API key', hide_input=True)
    
    save_api_key(api_key)
    click.echo('Configuration saved successfully!')

@cli.command()
@click.option('--preview', is_flag=True, help='Preview the commit message without committing')
def commit(preview):
    """Generate and apply a commit message for staged changes."""
    # Get API key
    api_key = get_api_key()
    if not api_key:
        raise click.ClickException(
            'No API key found. Please run `configure` command first or set ANTHROPIC_API_KEY environment variable.'
        )

    # Initialize Claude client
    client = anthropic.Client(api_key=api_key)

    # Get staged changes
    diff = get_staged_changes()
    if not diff:
        raise click.ClickException("No staged changes found.")

    # Generate commit message
    with click.progressbar(length=1, label='Generating commit message') as bar:
        commit_message = generate_commit_message(client, diff)
        bar.update(1)

    if preview:
        click.echo("\nGenerated commit message:")
        click.secho(commit_message, fg='green')
    else:
        try:
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            click.secho("\nSuccessfully committed with message:", fg='green')
            click.echo(commit_message)
        except subprocess.CalledProcessError as e:
            raise click.ClickException(f"Error executing git commit: {e}")

if __name__ == "__main__":
    cli()