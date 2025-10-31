"""
Configuration Manager
Loads settings from .env file and provides defaults.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()


class Config:
    """Central configuration for the project."""

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    # VLM Settings
    VLM_PROVIDER = os.getenv("VLM_PROVIDER", "mock")
    VLM_MODEL = os.getenv("VLM_MODEL", None)

    # Project Settings
    MAX_API_CALLS = int(os.getenv("MAX_API_CALLS", "100"))
    ATTACK_TEMPERATURE = float(os.getenv("ATTACK_TEMPERATURE", "0.9"))
    DEFENSE_TEMPERATURE = float(os.getenv("DEFENSE_TEMPERATURE", "0.3"))

    # Paths
    PROJECT_ROOT = Path(__file__).parent
    DATA_DIR = PROJECT_ROOT / "data"
    SAFE_IMAGES_DIR = DATA_DIR / "safe_images"
    ATTACK_IMAGES_DIR = DATA_DIR / "attack_images"
    DEFENSE_SCRIPTS_DIR = DATA_DIR / "defense_scripts"
    RESULTS_DIR = PROJECT_ROOT / "results"

    @classmethod
    def ensure_directories(cls):
        """Create all necessary directories."""
        for dir_path in [
            cls.DATA_DIR,
            cls.SAFE_IMAGES_DIR,
            cls.ATTACK_IMAGES_DIR,
            cls.DEFENSE_SCRIPTS_DIR,
            cls.RESULTS_DIR,
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def print_config(cls):
        """Print current configuration (hides API keys)."""
        print("=" * 70)
        print("CURRENT CONFIGURATION")
        print("=" * 70)
        print(f"VLM Provider:        {cls.VLM_PROVIDER}")
        print(f"VLM Model:           {cls.VLM_MODEL or '(using defaults)'}")
        print(f"OpenAI API Key:      {'✓ Set' if cls.OPENAI_API_KEY else '✗ Not set'}")
        print(
            f"Anthropic API Key:   {'✓ Set' if cls.ANTHROPIC_API_KEY else '✗ Not set'}"
        )
        print(f"Max API Calls:       {cls.MAX_API_CALLS}")
        print(f"Attack Temperature:  {cls.ATTACK_TEMPERATURE}")
        print(f"Defense Temperature: {cls.DEFENSE_TEMPERATURE}")
        print("=" * 70)

    @classmethod
    def is_mock_mode(cls):
        """Check if running in mock mode (no real APIs)."""
        return cls.VLM_PROVIDER == "mock"

    @classmethod
    def can_use_real_api(cls):
        """Check if real API can be used."""
        if cls.VLM_PROVIDER == "openai":
            return bool(cls.OPENAI_API_KEY)
        elif cls.VLM_PROVIDER == "anthropic":
            return bool(cls.ANTHROPIC_API_KEY)
        return False


if __name__ == "__main__":
    # Demo
    Config.print_config()

    if Config.is_mock_mode():
        print("\n⚠️  Running in MOCK mode")
        print("   No real API calls will be made")
        print("   To use real APIs:")
        print("   1. Edit .env file")
        print("   2. Add your API key")
        print("   3. Set VLM_PROVIDER to 'openai' or 'anthropic'")
    else:
        if Config.can_use_real_api():
            print(f"\n✅ Ready to use {Config.VLM_PROVIDER.upper()} API")
        else:
            print(f"\n⚠️  {Config.VLM_PROVIDER.upper()} selected but API key not found!")
            print("   Will fall back to mock mode")
