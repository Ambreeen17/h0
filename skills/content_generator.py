#!/usr/bin/env python3
"""
LinkedIn Content Generator - Silver Tier Business Use Case

Demonstrates practical business value by generating LinkedIn content.
AI Employee analyzes topics and creates professional posts.

Requirements:
- python-dotenv: pip install python-dotenv
"""

import os
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
CONTENT_FOLDER = Path('AI_Employee_Vault/Content')
LINKEDIN_DRAFTS = CONTENT_FOLDER / 'LinkedIn_Drafts'
PUBLISHED = CONTENT_FOLDER / 'Published'


class ContentGenerator:
    """Generates professional LinkedIn content."""

    def __init__(self):
        self.linkedin_drafts = LINKEDIN_DRAFTS
        self.published = PUBLISHED

        # Create folders
        self.linkedin_drafts.mkdir(parents=True, exist_ok=True)
        self.published.mkdir(parents=True, exist_ok=True)

    def generate_post(self, topic: str, tone: str = 'professional') -> dict:
        """
        Generate a LinkedIn post on a given topic.

        Args:
            topic: The topic to write about
            tone: professional, casual, inspirational, educational

        Returns:
            dict with generated content and metadata
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        # Select template based on tone
        if tone == 'professional':
            content = self.generate_professional_post(topic)
        elif tone == 'educational':
            content = self.generate_educational_post(topic)
        elif tone == 'inspirational':
            content = self.generate_inspirational_post(topic)
        else:
            content = self.generate_casual_post(topic)

        # Create content object
        post = {
            'topic': topic,
            'tone': tone,
            'content': content,
            'hashtags': self.generate_hashtags(topic),
            'created_at': timestamp,
            'status': 'draft'
        }

        return post

    def generate_professional_post(self, topic: str) -> str:
        """Generate a professional LinkedIn post."""
        return f"""🚀 {topic}

In today's rapidly evolving landscape, {topic.lower()} has become increasingly important for professionals and organizations alike.

Here are my thoughts on why this matters:

✅ Key Insight: {topic} represents a significant opportunity for growth and innovation.

✅ Practical Application: By leveraging {topic.lower()}, we can drive meaningful results and create lasting impact.

✅ Future Outlook: The potential for {topic.lower()} continues to expand as new technologies and methodologies emerge.

I'm curious to hear from others in the network:
👉 How are you approaching {topic.lower()} in your work?
👉 What challenges or successes have you experienced?

Let's discuss in the comments below. 👇

#{topic.replace(' ', '')} #Innovation #Growth #ProfessionalDevelopment"""

    def generate_educational_post(self, topic: str) -> str:
        """Generate an educational LinkedIn post."""
        return f"""📚 {topic}: A Quick Overview

I've been studying {topic.lower()} lately and wanted to share some key takeaways:

**What is it?**
{topic} is transforming how we approach problems and create solutions in our respective fields.

**Why it matters:**
→ Improves efficiency
→ Enables better decision-making
→ Creates new opportunities

**How to get started:**
1. Understand the fundamentals
2. Learn from practical examples
3. Apply in real-world scenarios

**Resources I recommend:**
- Industry publications
- Online courses
- Professional networks

What resources would you add to this list?

#{topic.replace(' ', '')} #Learning #Education #ProfessionalDevelopment"""

    def generate_inspirational_post(self, topic: str) -> str:
        """Generate an inspirational LinkedIn post."""
        return f"""✨ Embracing {topic}

Sometimes the most powerful step is simply deciding to begin.

{topic} isn't just about acquiring knowledge or skills—it's about transforming how we see ourselves and what we believe is possible.

Every expert was once a beginner.
Every leader started with a single step.
Every innovation began with a question.

If you're on the journey of mastering {topic.lower()}:
🌟 Remember: Progress over perfection
🌟 Celebrate small wins
🌟 Learn from setbacks
🌟 Keep moving forward

To my network: What's one piece of advice you'd give someone starting their journey with {topic.lower()}?

Drop it in the comments! 💬

#{topic.replace(' ', '')} #Motivation #Inspiration #GrowthMindset #Leadership"""

    def generate_casual_post(self, topic: str) -> str:
        """Generate a casual LinkedIn post."""
        return f"""Hey network! 👋

Been thinking about {topic} a lot lately.

Honestly? It's pretty fascinating stuff.

Here's what I've learned:
→ It's not as complicated as it seems
→ Small steps lead to big results
→ Community support makes all the difference

Would love to hear your thoughts and experiences!

Have you explored {topic.lower()}? What stood out to you?

👇 Comment below!

#{topic.replace(' ', '')} #Community #Learning #Growth"""

    def generate_hashtags(self, topic: str) -> list:
        """Generate relevant hashtags for the post."""
        base_tags = [
            f"#{topic.replace(' ', '')}",
            "#Innovation",
            "#Technology",
            "#Growth",
            "#Learning"
        ]

        # Add context-specific tags
        if 'AI' in topic or 'intelligence' in topic.lower():
            base_tags.extend(["#AI", "#MachineLearning", "#FutureOfWork"])

        if 'management' in topic.lower() or 'leadership' in topic.lower():
            base_tags.extend(["#Leadership", "#Management"])

        return base_tags[:8]  # LinkedIn recommends 3-5 hashtags, max 8

    def save_draft(self, post: dict) -> Path:
        """Save a post as a draft."""
        timestamp = datetime.now(timezone.utc).isoformat().replace(':', '-')[:19]
        filename = f"linkedin-draft-{timestamp}.md"
        filepath = self.linkedin_drafts / filename

        content = f"""# LinkedIn Post Draft

**Created**: {post['created_at']}
**Topic**: {post['topic']}
**Tone**: {post['tone']}
**Status**: {post['status']}

---

## Content

{post['content']}

## Hashtags

{' '.join(post['hashtags'])}

---

## Publishing Checklist

Before publishing:
- [ ] Review for clarity and tone
- [ ] Check for typos
- [ ] Verify hashtags are relevant
- [ ] Add call-to-action
- [ ] Include visual (optional but recommended)

## To Publish

1. Copy the content above
2. Go to: https://www.linkedin.com/feed/
3. Click "Start a post"
4. Paste content
5. Attach image if desired
6. Click "Post"

## After Publishing

Move this file to Published folder and update with:
- Published date
- Post URL
- Engagement metrics (likes, comments, shares)

---

*Generated by AI Employee - Silver Tier LinkedIn Content Generator*
"""

        filepath.write_text(content, encoding='utf-8')

        print(f"[OK] Draft saved: {filename}")
        print(f"[INFO] Topic: {post['topic']}")
        print(f"[INFO] Tone: {post['tone']}")

        return filepath

    def create_content_calendar(self, weeks: int = 4) -> Path:
        """
        Generate a content calendar with post ideas.

        Args:
            weeks: Number of weeks to generate content for
        """
        topics = [
            ('AI in the Workplace', 'professional'),
            ('Continuous Learning', 'inspirational'),
            ('Building Strong Teams', 'educational'),
            ('Innovation Strategies', 'professional'),
            ('Work-Life Balance', 'casual'),
            ('Leadership Development', 'educational'),
            ('Future of Work', 'professional'),
            ('Personal Growth', 'inspirational')
        ]

        timestamp = datetime.now(timezone.utc).isoformat()
        calendar_path = CONTENT_FOLDER / f'content-calendar-{timestamp[:10]}.md'

        content = f"""# LinkedIn Content Calendar

**Generated**: {timestamp}
**Duration**: {weeks} weeks
**Total Posts**: {weeks * len(topics)}

---

## Content Strategy

**Posting Frequency**: 2-3 times per week
**Best Times**: 9-10 AM, 2-3 PM, 5-6 PM (your audience's timezone)
**Content Mix**:
- 40% Educational (value and insights)
- 30% Professional (thought leadership)
- 20% Inspirational (motivation)
- 10% Casual (engagement)

---

## Week 1

"""

        # Generate posts for each week
        post_num = 1
        for week in range(1, weeks + 1):
            content += f"\n### Week {week}\n\n"

            for topic, tone in topics[:2]:  # 2 posts per week
                content += f"**Post {post_num}**: {topic}\n"
                content += f"- Tone: {tone}\n"
                content += f"- Status: To be generated\n"
                content += f"- Priority: {'High' if post_num <= 2 else 'Medium'}\n\n"
                post_num += 1

            content += "---\n\n"

        # Add post ideas section
        content += """## Additional Post Ideas

- Company milestones and achievements
- Behind-the-scenes content
- Team spotlights
- Industry news commentary
- Tips and best practices
- Lessons learned
- Book recommendations
- Event takeaways

## Engagement Strategy

- Respond to all comments within 24 hours
- Ask questions to encourage discussion
- Share relevant posts from others
- Tag people appropriately
- Use visual content when possible

## Metrics to Track

- Engagement rate (likes + comments + shares / impressions)
- Follower growth
- Profile views
- Post clicks
- Connection requests

---

*Content calendar generated by AI Employee*

Update this calendar as posts are published and track performance metrics.
"""

        calendar_path.write_text(content, encoding='utf-8')

        print(f"[OK] Content calendar created: {calendar_path.name}")
        print(f"[INFO] {weeks} weeks, {post_num-1} posts planned")

        return calendar_path


def main():
    """Main entry point for content generator."""
    import argparse

    parser = argparse.ArgumentParser(description='Generate LinkedIn content')
    parser.add_argument('--topic', required=True, help='Topic to write about')
    parser.add_argument('--tone', default='professional',
                       choices=['professional', 'casual', 'inspirational', 'educational'],
                       help='Tone of the post')
    parser.add_argument('--calendar', type=int, metavar='WEEKS',
                       help='Generate content calendar for N weeks')
    args = parser.parse_args()

    generator = ContentGenerator()

    if args.calendar:
        generator.create_content_calendar(args.calendar)
        return

    # Generate single post
    post = generator.generate_post(args.topic, args.tone)
    filepath = generator.save_draft(post)

    print(f"\n[OK] Draft saved to: {filepath}")
    print(f"[INFO] Ready for review and publishing!")


if __name__ == '__main__':
    main()
