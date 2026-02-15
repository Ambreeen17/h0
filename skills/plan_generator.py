#!/usr/bin/env python3
"""
Plan Generator - Silver Tier Structured Reasoning

Agent Skill for generating Plan.md files for complex multi-step tasks.
Provides structured reasoning and execution tracking.

Requirements:
- python-dotenv: pip install python-dotenv
"""

import os
import re
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
NEEDS_ACTION_FOLDER = os.getenv('VAULT_NEEDS_ACTION', 'AI_Employee_Vault/Needs_Action')
PLAN_FOLDER = os.getenv('VAULT_PLAN', 'AI_Employee_Vault/Plans')


class PlanGenerator:
    """Generates Plan.md files for complex tasks."""

    def __init__(self):
        self.needs_action_path = Path(NEEDS_ACTION_FOLDER)
        self.plan_path = Path(PLAN_FOLDER)
        self.plan_path.mkdir(parents=True, exist_ok=True)

    def read_task(self, task_path: Path) -> str:
        """Read task file content."""
        with open(task_path, 'r', encoding='utf-8') as f:
            return f.read()

    def parse_task(self, content: str) -> dict:
        """Extract task information."""
        task_info = {
            'title': '',
            'type': '',
            'source': '',
            'description': '',
            'context': ''
        }

        # Extract title
        for line in content.split('\n')[:5]:
            if line.startswith('# '):
                task_info['title'] = line.lstrip('#').strip()
                break

        # Extract metadata
        for line in content.split('\n'):
            if '**Type**:' in line:
                task_info['type'] = line.split(':', 1)[1].strip()
            elif '**Source**:' in line:
                task_info['source'] = line.split(':', 1)[1].strip()
            elif '**Priority**:' in line:
                task_info['priority'] = line.split(':', 1)[1].strip()

        # Extract description
        if '## Description' in content:
            desc_section = content.split('## Description')[1].split('##')[0]
            task_info['description'] = desc_section.strip()

        # Extract context
        if '## Context' in content:
            ctx_section = content.split('## Context')[1].split('##')[0]
            task_info['context'] = ctx_section.strip()

        return task_info

    def assess_complexity(self, task_info: dict) -> dict:
        """
        Assess task complexity and determine if a plan is needed.
        Returns complexity score and recommendation.
        """
        complexity_score = 0
        reasons = []

        # Check description length
        if len(task_info['description']) > 500:
            complexity_score += 2
            reasons.append("Long description (detailed task)")

        # Check for multiple action items
        action_keywords = ['and then', 'after that', 'next', 'finally', 'also', 'additionally']
        action_count = sum(1 for keyword in action_keywords if keyword in task_info['description'].lower())
        if action_count >= 2:
            complexity_score += 3
            reasons.append(f"Multiple action items detected ({action_count})")

        # Check for specific complexity indicators
        complexity_indicators = [
            'research', 'investigate', 'analyze', 'create', 'build', 'implement',
            'coordinate', 'organize', 'manage', 'design', 'develop'
        ]
        for indicator in complexity_indicators:
            if indicator in task_info['description'].lower():
                complexity_score += 1
                reasons.append(f"Complex action: {indicator}")

        # Check task type
        if task_info['type'] == 'user-request':
            complexity_score += 2
            reasons.append("Direct user request (may need planning)")

        # Determine if plan is needed
        needs_plan = complexity_score >= 3

        return {
            'score': complexity_score,
            'needs_plan': needs_plan,
            'reasons': reasons
        }

    def generate_plan_content(self, task_info: dict, task_path: Path) -> str:
        """Generate Plan.md content for a task."""
        timestamp = datetime.now(timezone.utc).isoformat()
        task_name = task_path.stem

        # Generate steps based on task analysis
        steps = self.generate_steps(task_info)

        plan_content = f"""# Execution Plan: {task_info['title']}

**Created**: {timestamp}
**Task File**: `{task_path.name}`
**Status**: pending
**Complexity Score**: {task_info.get('complexity_score', 0)}
**Type**: {task_info['type']}
**Source**: {task_info['source']}

---

## Overview

{task_info['description']}

### Context

{task_info['context'] if task_info['context'] else 'No additional context provided.'}

---

## Analysis

### Complexity Assessment

{chr(10).join(f"- {reason}" for reason in task_info.get('complexity_reasons', ['Standard task']))}

### Estimated Duration

30-60 minutes

---

## Execution Plan

## Phase 1: Preparation

- [ ] **P1**: Review task requirements and context
- [ ] **P2**: Identify required resources and tools
- [ ] **P3**: Define success criteria

## Phase 2: Execution

{chr(10).join(f"- [ ] **{i+1}**: {step}" for i, step in enumerate(steps))}

## Phase 3: Verification

- [ ] **V1**: Review completed work against requirements
- [ ] **V2**: Test and validate results
- [ ] **V3**: Document outcomes and learnings

---

## Status Tracking

### Progress

0/3 phases completed

### Current Phase

Preparation

### Blockers

None identified

### Notes

*Updates will be added as execution progresses*

---

## Completion Checklist

- [ ] All preparation steps completed
- [ ] All execution steps completed
- [ ] All verification steps completed
- [ ] Task moved to Done folder
- [ ] Dashboard updated

---

**Last Updated**: {timestamp}
**Plan Status**: Draft - Ready for execution

---

*This plan was automatically generated by the PlanGenerator Agent Skill.
Update this plan as execution progresses to maintain accurate tracking.*
"""

        return plan_content

    def generate_steps(self, task_info: dict) -> list:
        """Generate execution steps based on task type and content."""
        steps = []

        # Default steps based on task type
        if 'email' in task_info['type'].lower() or task_info['source'] == 'EmailWatcher':
            steps = [
                "Read and understand email content",
                "Identify sender intent and urgency",
                "Draft appropriate response if needed",
                "Categorize email for future reference",
                "Update task with processing results"
            ]
        elif 'file' in task_info['type'].lower() or task_info['source'] == 'FileSystemWatcher':
            steps = [
                "Analyze file content and metadata",
                "Determine file purpose and category",
                "Extract key information or insights",
                "Perform required actions based on file type",
                "Log findings and update system"
            ]
        else:
            steps = [
                "Analyze task requirements",
                "Identify necessary actions",
                "Execute primary task activities",
                "Validate results",
                "Document completion"
            ]

        return steps

    def generate_plan_for_task(self, task_path: Path) -> Path:
        """Generate a plan for a specific task."""
        content = self.read_task(task_path)
        task_info = self.parse_task(content)

        # Assess complexity
        complexity = self.assess_complexity(task_info)
        task_info['complexity_score'] = complexity['score']
        task_info['complexity_reasons'] = complexity['reasons']

        # Only create plan if complexity warrants it
        if not complexity['needs_plan']:
            print(f"[SKIP] Task {task_path.name} is simple (score: {complexity['score']})")
            return None

        # Generate plan
        plan_content = self.generate_plan_content(task_info, task_path)

        # Save plan
        plan_filename = f"plan-{task_path.stem}.md"
        plan_path = self.plan_path / plan_filename

        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(plan_content)

        print(f"[✓] Plan created: {plan_filename} (complexity: {complexity['score']})")

        return plan_path

    def generate_plans_for_all(self) -> list:
        """Generate plans for all complex tasks in Needs_Action."""
        tasks = list(self.needs_action_path.glob('task-*.md'))
        plans_created = []

        print(f"[INFO] Analyzing {len(tasks)} tasks for complexity...")

        for task_path in tasks:
            try:
                plan_path = self.generate_plan_for_task(task_path)
                if plan_path:
                    plans_created.append(plan_path)
            except Exception as e:
                print(f"[ERROR] Failed to generate plan for {task_path.name}: {e}")

        return plans_created


def main():
    """Main entry point for plan generator."""
    import argparse

    parser = argparse.ArgumentParser(description='Generate execution plans for tasks')
    parser.add_argument('--all', action='store_true', help='Generate plans for all complex tasks')
    parser.add_argument('--task', type=str, help='Generate plan for specific task')
    args = parser.parse_args()

    generator = PlanGenerator()

    if args.all:
        plans = generator.generate_plans_for_all()
        print(f"\n[SUMMARY] Generated {len(plans)} plans")
        return

    if args.task:
        task_path = Path(NEEDS_ACTION_FOLDER) / args.task
        if task_path.exists():
            generator.generate_plan_for_task(task_path)
        else:
            print(f"[ERROR] Task not found: {args.task}")
        return

    # Default: show help
    parser.print_help()


if __name__ == '__main__':
    main()
