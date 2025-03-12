"""Theme management for the book tracking app."""
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class ThemeColors:
    """Represents the colors used in a theme."""
    bg: str  # Main background
    bg1: str  # Secondary background
    bg2: str  # Tertiary background
    fg: str  # Main text
    fg1: str  # Secondary text
    accent: str  # Primary accent color
    accent_hover: str  # Hover state for accent
    success: str  # Success/positive color
    error: str  # Error/negative color

# Built-in themes
THEMES: Dict[str, ThemeColors] = {
    "gruvbox-dark": ThemeColors(
        bg="#282828",  # Background
        bg1="#3c3836",  # Secondary Background
        bg2="#504945",  # Tertiary Background
        fg="#ebdbb2",  # Text
        fg1="#d5c4a1",  # Secondary Text
        accent="#83a598",  # Blue for links/buttons
        accent_hover="#8ec07c",  # Aqua for hover states
        success="#b8bb26",  # Green
        error="#fb4934"  # Red
    ),
    "light": ThemeColors(
        bg="#ffffff",
        bg1="#f3f4f6",
        bg2="#e5e7eb",
        fg="#111827",
        fg1="#4b5563",
        accent="#3b82f6",
        accent_hover="#2563eb",
        success="#10b981",
        error="#ef4444"
    )
}

def get_theme(name: str) -> Optional[ThemeColors]:
    """Get a theme by name."""
    return THEMES.get(name)
