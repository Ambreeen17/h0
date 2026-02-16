#!/usr/bin/env python3
"""
Video Practice Script - AI Employee Vault
Helps you rehearse the hackathon video before recording

Usage:
    python video_practice.py
"""

import time
import os
from pathlib import Path

def print_section(title):
    """Print a section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)
    print()

def countdown(seconds):
    """Countdown timer."""
    for i in range(seconds, 0, -1):
        print(f"   [{i}] ", end="", flush=True)
        time.sleep(1)
    print("\n")

def practice_intro():
    """Practice intro section."""
    print_section("PART 1: INTRODUCTION (1 minute)")

    print("📹 ACTION: Face camera or show title slide")
    print()
    print("🗣️ SAY THIS:")
    print('   "Hi judges, I\'m presenting AI Employee Vault for Hackathon 0."')
    print('   "This is a Platinum tier autonomous AI employee system"')
    print('   "built with Claude Code. Let me show you what it can do."')
    print()
    print("⏱️  Practice for 30 seconds...")
    countdown(30)
    print("✅ Done! Move to next section.")

def practice_readme():
    """Practice README section."""
    print_section("PART 2: SHOW README (1 minute)")

    print("📹 ACTION: Open VS Code → README.md")
    print("📁 FILE: C:\\HACKATHON 0\\README.md")
    print()
    print("🎯 SHOW THESE SECTIONS:")
    print("   • Scroll to top - show title")
    print("   • Tier Declaration section")
    print("   • System Architecture (brief)")
    print("   • Quickstart section")
    print()
    print("🗣️ SAY THIS:")
    print('   "The project is a Digital Full-Time Equivalent AI employee."')
    print('   "It has four tiers: Bronze, Silver, Gold, and Platinum."')
    print('   "I\'ve completed all Platinum tier requirements including')
    print('   "hybrid cloud/local architecture, delegation system,')
    print('   "and production-ready security."')
    print()
    print("⏱️  Practice for 30 seconds...")
    countdown(30)
    print("✅ Done! Move to next section.")

def practice_health_check():
    """Practice health check section."""
    print_section("PART 3: HEALTH CHECK (30 seconds)")

    print("📹 ACTION: Open Terminal")
    print("💻 COMMAND:")
    print("   cd C:\\HACKATHON 0")
    print("   python skills/health_monitor.py --summary")
    print()
    print("🎯 SHOW: Output showing all 'healthy'")
    print()
    print("🗣️ SAY THIS:")
    print('   "First, let me verify the system is healthy."')
    print('   "All services are operational - cloud zone, local zone,')
    print('   "zone synchronization, everything is healthy."')
    print()
    print("⏱️  Practice for 20 seconds...")
    countdown(20)
    print("✅ Done! Move to next section.")

def practice_tests():
    """Practice tests section."""
    print_section("PART 4: RUN TESTS (1 minute)")

    print("📹 ACTION: Use SAME terminal or open new one")
    print("💻 COMMAND:")
    print("   python tests/test_suite.py --all")
    print()
    print("🎯 SHOW: Tests running, '20/20 passed' message")
    print()
    print("🗣️ SAY THIS:")
    print('   "I\'ve created a comprehensive test suite with 20 tests')
    print('   "covering all components. Let me run it now."')
    print('   "All 20 tests pass - this validates cloud zone operations,')
    print('   "local zone approvals, zone synchronization, health monitoring,')
    print('   "and the complete end-to-end workflow."')
    print()
    print("⏱️  Practice for 30 seconds...")
    countdown(30)
    print("✅ Done! Move to next section.")

def practice_cloud_zone():
    """Practice cloud zone section."""
    print_section("PART 5: CLOUD ZONE (30 seconds)")

    print("📹 ACTION: Open NEW terminal window")
    print("💻 COMMAND:")
    print("   python skills/cloud_zone_manager.py --status")
    print()
    print("🎯 SHOW: JSON output with capabilities")
    print()
    print("🗣️ SAY THIS:")
    print('   "The cloud zone operates 24/7 handling drafting,')
    print('   "triage, and analysis. It can process tasks without')
    print('   "needing human intervention."')
    print()
    print("⏱️  Practice for 20 seconds...")
    countdown(20)
    print("✅ Done! Move to next section.")

def practice_local_zone():
    """Practice local zone section."""
    print_section("PART 6: LOCAL ZONE (30 seconds)")

    print("📹 ACTION: Use SAME terminal")
    print("💻 COMMAND:")
    print("   python skills/local_zone_manager.py --status")
    print()
    print("🎯 SHOW: Security rules, approvals")
    print()
    print("🗣️ SAY THIS:")
    print('   "The local zone handles sensitive operations like')
    print('   "approvals, banking, and credential access."')
    print('   "It enforces human-in-the-loop oversight."')
    print()
    print("⏱️  Practice for 20 seconds...")
    countdown(20)
    print("✅ Done! Move to next section.")

def practice_documentation():
    """Practice documentation section."""
    print_section("PART 7: DOCUMENTATION (30 seconds)")

    print("📹 ACTION: VS Code → docs/ARCHITECTURE_DIAGRAMS.md")
    print("📁 FILE: C:\\HACKATHON 0\\docs\\ARCHITECTURE_DIAGRAMS.md")
    print()
    print("🎯 SHOW: Scroll through Mermaid diagrams")
    print()
    print("🗣️ SAY THIS:")
    print('   "I\'ve created comprehensive documentation including')
    print('   "15 architecture diagrams showing the complete system design,')
    print('   "security boundaries, and data flow."')
    print()
    print("⏱️  Practice for 20 seconds...")
    countdown(20)
    print("✅ Done! Move to next section.")

def practice_github():
    """Practice GitHub section."""
    print_section("PART 8: GITHUB (1 minute)")

    print("📹 ACTION: Browser → https://github.com/Ambreeen17/h0")
    print()
    print("🎯 SHOW:")
    print("   • README (scroll through)")
    print("   • Click 'Code' tab")
    print("   • Show skills/ folder")
    print("   • Click 'commits'")
    print("   • Show recent commits")
    print()
    print("🗣️ SAY THIS:")
    print('   "The complete source code is available on GitHub.')
    print('   "You can see the comprehensive README and project structure."')
    print('   "The git history shows professional commit practices.')
    print()
    print("⏱️  Practice for 40 seconds...")
    countdown(40)
    print("✅ Done! Move to next section.")

def practice_conclusion():
    """Practice conclusion section."""
    print_section("PART 9: CONCLUSION (30 seconds)")

    print("📹 ACTION: Face camera or show final slide")
    print()
    print("🗣️ SAY THIS:")
    print('   "To summarize, AI Employee Vault is a production-ready')
    print('   "Digital FTE system with:')
    print()
    print('   "✅ Complete Platinum tier implementation"')
    print('   "✅ Hybrid cloud/local architecture"')
    print('   "✅ Secure delegation system"')
    print('   "✅ Human-in-the-loop oversight"')
    print('   "✅ Comprehensive testing (20/20 tests passing)"')
    print('   "✅ Professional documentation"')
    print()
    print('   "It demonstrates how AI agents can operate as')
    print('   "structured autonomous employees, not just chatbots."')
    print()
    print('   "Thank you for watching!"')
    print()
    print("⏱️  Practice for 30 seconds...")
    countdown(30)
    print("✅ Done! Practice complete!")

def main():
    """Run the practice session."""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                                ║
║        🎬 VIDEO PRACTICE SESSION - AI Employee Vault           ║
║                                                                ║
║  This will guide you through each section with timing         ║
║  so you can practice before the actual recording.            ║
║                                                                ║
╚═══════════════════════════════════════════════════════════════╝
""")

    print("\n📋 PRACTICE MODE")
    print("\nThis will guide you through each section:")
    print("- What to say")
    print("- What to show")
    print("- How long to practice each part")
    print("\n⚠️  Note: This is for practice only - not recording yet!")
    print("\nPress Enter to start practice session...")
    input()

    # Run through all sections
    practice_intro()
    time.sleep(2)

    practice_readme()
    time.sleep(2)

    practice_health_check()
    time.sleep(2)

    practice_tests()
    time.sleep(2)

    practice_cloud_zone()
    time.sleep(2)

    practice_local_zone()
    time.sleep(2)

    practice_documentation()
    time.sleep(2)

    practice_github()
    time.sleep(2)

    practice_conclusion()

    # Summary
    print("\n" + "="*70)
    print("  ✅ PRACTICE COMPLETE!")
    print("="*70)
    print()
    print("You've practiced all sections. Total practice time: ~5 minutes")
    print()
    print("🎯 NEXT STEPS:")
    print("   1. If you felt rushed, practice again")
    print("   2. Open all files in VS Code tabs")
    print("   3. Open GitHub in browser")
    print("   4. When ready, record for real!")
    print()
    print("💡 TIP: The second time through will be much smoother!")
    print()
    print("📹 TO RECORD FOR REAL:")
    print("   1. Press Win + G")
    print("   2. Click 'Start recording'")
    print("   3. Follow the same sequence")
    print("   4. Press Win + Alt + R to stop")
    print()
    print("="*70)
    print()

if __name__ == "__main__":
    main()
