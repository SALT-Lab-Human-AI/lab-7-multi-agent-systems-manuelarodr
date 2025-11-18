"""
Excercise 4: Marketing Strategy Development System
================================================================

This implementation uses CrewAI to develop comprehensive marketing strategies
for products through a collaborative multi-agent workflow.

Agents:
1. MarketResearchAgent - Market Research Analyst (analyzes target market, competitors, personas)
2. ContentStrategistAgent - Content Strategist (develops messaging and content themes)
3. ChannelSpecialistAgent - Marketing Channel Specialist (identifies best channels and tactics)
4. CampaignPlannerAgent - Campaign Planner (creates specific campaign plans and timelines)
5. BudgetAnalystAgent - Marketing Budget Analyst (allocates budget and calculates ROI)

Configuration:
- Uses shared configuration from the root .env file
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from crewai import Agent, Task, Crew
from crewai.tools import tool

# Add parent directory to path to import shared_config
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import shared configuration
from shared_config import Config, validate_config


# ============================================================================
# TOOLS (Research and analysis tools for marketing)
# ============================================================================

@tool
def research_market_trends(product_category: str, target_audience: str) -> str:
    """
    Research current market trends and consumer behavior for a product category.
    Provides insights on market size, growth trends, and consumer preferences.
    """
    return f"""
    Research task: Analyze market trends for {product_category} targeting {target_audience}.
    
    Please research and provide:
    1. Current market size and growth projections
    2. Key consumer trends and preferences
    3. Emerging market opportunities
    4. Seasonal patterns and buying behaviors
    5. Demographic and psychographic insights
    6. Market challenges and barriers
    
    Focus on actionable insights for marketing strategy development.
    """


@tool
def analyze_competitors(product_name: str, product_category: str) -> str:
    """
    Analyze competitor marketing strategies and positioning.
    Identifies competitor strengths, weaknesses, and marketing approaches.
    """
    return f"""
    Research task: Analyze competitors for {product_name} in {product_category}.
    
    Please research and provide:
    1. Main competitors and their market positioning
    2. Competitor marketing messages and value propositions
    3. Competitor channel strategies (social media, advertising, content)
    4. Competitor pricing strategies
    5. Competitor strengths and weaknesses
    6. Market gaps and differentiation opportunities
    
    Focus on insights that inform competitive marketing strategy.
    """


@tool
def research_marketing_channels(product_category: str, target_audience: str) -> str:
    """
    Research effective marketing channels for reaching target audience.
    Provides channel performance data and best practices.
    """
    return f"""
    Research task: Identify best marketing channels for {product_category} targeting {target_audience}.
    
    Please research and provide:
    1. Most effective channels for this audience (social media, email, SEO, paid ads, etc.)
    2. Channel performance benchmarks and costs
    3. Best practices for each channel
    4. Channel integration strategies
    5. Emerging channel opportunities
    6. Channel-specific content requirements
    
    Focus on channels that deliver the best ROI for this product and audience.
    """


@tool
def calculate_marketing_metrics(budget: float, channels: str) -> str:
    """
    Calculate expected marketing metrics and ROI for a given budget and channel mix.
    Provides cost estimates, reach projections, and performance benchmarks.
    """
    return f"""
    Analysis task: Calculate marketing metrics for ${budget:,.0f} budget across {channels}.
    
    Please provide:
    1. Budget allocation recommendations per channel
    2. Expected reach and impressions
    3. Estimated cost per acquisition (CPA)
    4. Projected conversion rates
    5. ROI estimates and benchmarks
    6. Performance tracking recommendations
    
    Use industry benchmarks and realistic projections.
    """


# ============================================================================
# AGENT DEFINITIONS
# ============================================================================

def create_market_research_agent(product_name: str, product_category: str):
    """Create the Market Research Analyst agent."""
    return Agent(
        role="Market Research Analyst",
        goal=f"Conduct comprehensive market research for {product_name} in the {product_category} category. "
             f"Analyze target market, competitors, customer personas, and market opportunities. "
             f"Provide actionable insights that inform the marketing strategy.",
        backstory=(
            f"You are a senior market research analyst with 10+ years of experience in {product_category} markets. "
            f"You excel at identifying market trends, understanding consumer behavior, and analyzing competitive landscapes. "
            f"You have a proven track record of uncovering insights that drive successful marketing strategies. "
            f"You use data-driven approaches and always validate your findings with multiple sources. "
            f"Your research is thorough, accurate, and focused on actionable insights for marketing teams."
        ),
        tools=[research_market_trends, analyze_competitors],
        verbose=True,
        allow_delegation=False
    )


def create_content_strategist_agent(product_name: str, target_audience: str):
    """Create the Content Strategist agent."""
    return Agent(
        role="Content Strategist",
        goal=f"Develop compelling messaging, content themes, and brand voice for {product_name} "
             f"targeting {target_audience}. Create content strategies that resonate with the target audience "
             f"and differentiate the product in the market.",
        backstory=(
            f"You are an expert content strategist specializing in {target_audience} marketing. "
            f"You have a deep understanding of how to craft messages that connect with audiences emotionally and logically. "
            f"You excel at developing brand voices, content themes, and messaging frameworks that drive engagement and conversions. "
            f"You understand the nuances of different content formats and how to adapt messaging across channels. "
            f"Your strategies are creative, data-informed, and aligned with business objectives."
        ),
        tools=[research_market_trends],
        verbose=True,
        allow_delegation=False
    )


def create_channel_specialist_agent(product_category: str, target_audience: str):
    """Create the Marketing Channel Specialist agent."""
    return Agent(
        role="Marketing Channel Specialist",
        goal=f"Identify the most effective marketing channels and tactics for {product_category} "
             f"targeting {target_audience}. Recommend channel strategies that maximize reach, engagement, and ROI.",
        backstory=(
            f"You are a marketing channel expert with extensive experience in {product_category} marketing. "
            f"You understand the strengths and limitations of each marketing channel (social media, email, SEO, PPC, content, etc.). "
            f"You know which channels work best for different audiences and how to integrate multiple channels effectively. "
            f"You stay current with channel trends, algorithm changes, and emerging opportunities. "
            f"Your recommendations are based on data, industry best practices, and proven results."
        ),
        tools=[research_marketing_channels],
        verbose=True,
        allow_delegation=False
    )


def create_campaign_planner_agent(product_name: str, target_audience: str):
    """Create the Campaign Planner agent."""
    return Agent(
        role="Campaign Planner",
        goal=f"Create detailed, actionable marketing campaign plans for {product_name} targeting {target_audience}. "
             f"Develop campaign timelines, tactics, and execution strategies that align with marketing objectives.",
        backstory=(
            f"You are a strategic campaign planner with expertise in developing end-to-end marketing campaigns. "
            f"You excel at translating marketing strategies into actionable campaign plans with clear timelines and milestones. "
            f"You understand how to sequence activities, coordinate across channels, and optimize for maximum impact. "
            f"You create realistic timelines, identify dependencies, and plan for contingencies. "
            f"Your campaigns are well-structured, measurable, and designed for success."
        ),
        tools=[],
        verbose=True,
        allow_delegation=False
    )


def create_budget_analyst_agent(product_category: str):
    """Create the Marketing Budget Analyst agent."""
    return Agent(
        role="Marketing Budget Analyst",
        goal=f"Allocate marketing budget effectively across channels and activities for {product_category} products. "
             f"Calculate ROI projections, cost estimates, and provide budget optimization recommendations.",
        backstory=(
            f"You are a marketing finance expert specializing in budget allocation and ROI analysis for {product_category} markets. "
            f"You have deep knowledge of marketing costs, performance benchmarks, and ROI calculations. "
            f"You excel at optimizing budget allocation to maximize marketing effectiveness. "
            f"You understand the relationship between spend and results across different channels and tactics. "
            f"Your budget recommendations are data-driven, realistic, and focused on achieving marketing objectives efficiently."
        ),
        tools=[calculate_marketing_metrics],
        verbose=True,
        allow_delegation=False
    )


# ============================================================================
# TASK DEFINITIONS
# ============================================================================

def create_market_research_task(market_research_agent, product_name: str, product_category: str, 
                                target_audience: str, product_description: str):
    """Create the market research task."""
    return Task(
        description=(
            f"Conduct comprehensive market research for {product_name} ({product_category}). "
            f"Product description: {product_description}. "
            f"Target audience: {target_audience}. "
            f"\n\nYour research should include:\n"
            f"1. Target market analysis (size, demographics, psychographics, behaviors)\n"
            f"2. Competitive landscape analysis (main competitors, their positioning, strengths/weaknesses)\n"
            f"3. Customer persona development (2-3 detailed personas)\n"
            f"4. Market opportunities and gaps\n"
            f"5. Key market trends affecting this product category\n"
            f"6. Market challenges and barriers to entry\n\n"
            f"Provide actionable insights that will inform the marketing strategy."
        ),
        agent=market_research_agent,
        expected_output=(
            f"A comprehensive market research report including target market analysis, "
            f"competitive landscape, customer personas, market opportunities, trends, and challenges "
            f"for {product_name} in the {product_category} category."
        )
    )


def create_content_strategy_task(content_strategist_agent, product_name: str, product_description: str,
                                target_audience: str, unique_value_proposition: str):
    """Create the content strategy task."""
    return Task(
        description=(
            f"Develop a comprehensive content strategy for {product_name}. "
            f"Product: {product_description}. "
            f"Target audience: {target_audience}. "
            f"Unique value proposition: {unique_value_proposition}. "
            f"\n\nYour content strategy should include:\n"
            f"1. Core messaging framework (key messages, value propositions, differentiators)\n"
            f"2. Brand voice and tone guidelines\n"
            f"3. Content themes and topics (5-7 main themes)\n"
            f"4. Content formats and types (blog posts, videos, social media, etc.)\n"
            f"5. Content pillars that support marketing objectives\n"
            f"6. Messaging variations for different channels and audiences\n\n"
            f"Ensure messaging resonates with the target audience and differentiates the product."
        ),
        agent=content_strategist_agent,
        expected_output=(
            f"A comprehensive content strategy document including messaging framework, "
            f"brand voice, content themes, formats, and channel-specific messaging for {product_name}."
        )
    )


def create_channel_strategy_task(channel_specialist_agent, product_name: str, product_category: str,
                                target_audience: str, marketing_objectives: str):
    """Create the channel strategy task."""
    return Task(
        description=(
            f"Develop a marketing channel strategy for {product_name} ({product_category}). "
            f"Target audience: {target_audience}. "
            f"Marketing objectives: {marketing_objectives}. "
            f"\n\nYour channel strategy should include:\n"
            f"1. Recommended marketing channels (prioritized list with rationale)\n"
            f"2. Channel-specific tactics and approaches\n"
            f"3. Channel integration strategy (how channels work together)\n"
            f"4. Channel performance expectations and KPIs\n"
            f"5. Channel-specific content requirements\n"
            f"6. Emerging channel opportunities\n\n"
            f"Focus on channels that best reach the target audience and achieve marketing objectives."
        ),
        agent=channel_specialist_agent,
        expected_output=(
            f"A comprehensive channel strategy document including recommended channels, "
            f"tactics, integration approach, KPIs, and content requirements for {product_name}."
        )
    )


def create_campaign_plan_task(campaign_planner_agent, product_name: str, target_audience: str,
                              campaign_timeline: str, marketing_objectives: str):
    """Create the campaign planning task."""
    return Task(
        description=(
            f"Create a detailed marketing campaign plan for {product_name} targeting {target_audience}. "
            f"Campaign timeline: {campaign_timeline}. "
            f"Marketing objectives: {marketing_objectives}. "
            f"\n\nYour campaign plan should include:\n"
            f"1. Campaign phases and timeline (with specific dates/milestones)\n"
            f"2. Campaign tactics and activities for each phase\n"
            f"3. Channel-specific campaign activities\n"
            f"4. Success metrics and KPIs for each phase\n"
            f"5. Resource requirements and dependencies\n"
            f"6. Risk mitigation strategies\n"
            f"7. Campaign launch checklist\n\n"
            f"Create an actionable, realistic campaign plan that can be executed."
        ),
        agent=campaign_planner_agent,
        expected_output=(
            f"A detailed marketing campaign plan including phases, timeline, tactics, "
            f"metrics, resources, and execution strategy for {product_name}."
        )
    )


def create_budget_allocation_task(budget_analyst_agent, product_name: str, total_budget: float,
                                  marketing_objectives: str, campaign_timeline: str):
    """Create the budget allocation task."""
    return Task(
        description=(
            f"Allocate marketing budget for {product_name} campaign. "
            f"Total budget: ${total_budget:,.0f}. "
            f"Marketing objectives: {marketing_objectives}. "
            f"Campaign timeline: {campaign_timeline}. "
            f"\n\nYour budget allocation should include:\n"
            f"1. Budget breakdown by channel (with percentages and dollar amounts)\n"
            f"2. Budget allocation by campaign phase/timeline\n"
            f"3. Cost estimates for key activities (advertising, content creation, tools, etc.)\n"
            f"4. Expected ROI and performance metrics for each channel\n"
            f"5. Budget optimization recommendations\n"
            f"6. Contingency planning (10-15% buffer)\n"
            f"7. Cost-saving opportunities\n\n"
            f"Ensure budget allocation maximizes ROI and supports marketing objectives."
        ),
        agent=budget_analyst_agent,
        expected_output=(
            f"A comprehensive budget allocation plan including channel breakdown, "
            f"timeline allocation, cost estimates, ROI projections, and optimization recommendations "
            f"for the {product_name} marketing campaign."
        )
    )


# ============================================================================
# CREW ORCHESTRATION
# ============================================================================

def main(product_name: str = "AI-Powered Task Manager",
         product_category: str = "Productivity Software",
         product_description: str = "An AI-powered task management application that helps teams organize, prioritize, and complete work more efficiently",
         target_audience: str = "Small to medium-sized business teams and remote workers",
         unique_value_proposition: str = "Intelligent task prioritization using AI, seamless team collaboration, and automated workflow optimization",
         marketing_objectives: str = "Increase brand awareness, generate qualified leads, and drive product sign-ups",
         campaign_timeline: str = "3 months (Q1 launch campaign)",
         total_budget: float = 50000.0):
    """
    Main function to orchestrate the marketing strategy development crew.

    Args:
        product_name: Name of the product
        product_category: Category/industry of the product
        product_description: Brief description of what the product does
        target_audience: Primary target audience for the product
        unique_value_proposition: What makes the product unique
        marketing_objectives: Primary marketing goals
        campaign_timeline: Timeline for the marketing campaign
        total_budget: Total marketing budget in dollars
    """

    print("=" * 80)
    print("CrewAI Multi-Agent Marketing Strategy Development System")
    print("=" * 80)
    print()
    print(f"📦 Product: {product_name}")
    print(f"🏷️  Category: {product_category}")
    print(f"🎯 Target Audience: {target_audience}")
    print(f"💰 Budget: ${total_budget:,.0f}")
    print(f"📅 Timeline: {campaign_timeline}")
    print()

    # Validate configuration
    print("🔍 Validating configuration...")
    if not validate_config():
        print("❌ Configuration validation failed. Please set up your .env file.")
        exit(1)

    # Set environment variables for CrewAI
    os.environ["OPENAI_API_KEY"] = Config.API_KEY
    os.environ["OPENAI_API_BASE"] = Config.API_BASE
    
    if Config.USE_GROQ:
        os.environ["OPENAI_MODEL_NAME"] = Config.OPENAI_MODEL

    print("✅ Configuration validated successfully!")
    print()
    Config.print_summary()
    print()

    # Create agents
    print("[1/5] Creating Market Research Analyst Agent...")
    market_research_agent = create_market_research_agent(product_name, product_category)

    print("[2/5] Creating Content Strategist Agent...")
    content_strategist_agent = create_content_strategist_agent(product_name, target_audience)

    print("[3/5] Creating Marketing Channel Specialist Agent...")
    channel_specialist_agent = create_channel_specialist_agent(product_category, target_audience)

    print("[4/5] Creating Campaign Planner Agent...")
    campaign_planner_agent = create_campaign_planner_agent(product_name, target_audience)

    print("[5/5] Creating Marketing Budget Analyst Agent...")
    budget_analyst_agent = create_budget_analyst_agent(product_category)

    print("\n✅ All agents created successfully!")
    print()

    # Create tasks
    print("Creating tasks for the crew...")
    market_research_task = create_market_research_task(
        market_research_agent, product_name, product_category, target_audience, product_description
    )
    
    content_strategy_task = create_content_strategy_task(
        content_strategist_agent, product_name, product_description, target_audience, unique_value_proposition
    )
    
    channel_strategy_task = create_channel_strategy_task(
        channel_specialist_agent, product_name, product_category, target_audience, marketing_objectives
    )
    
    campaign_plan_task = create_campaign_plan_task(
        campaign_planner_agent, product_name, target_audience, campaign_timeline, marketing_objectives
    )
    
    budget_allocation_task = create_budget_allocation_task(
        budget_analyst_agent, product_name, total_budget, marketing_objectives, campaign_timeline
    )

    print("Tasks created successfully!")
    print()

    # Create the crew with sequential task execution
    print("Forming the Marketing Strategy Crew...")
    crew = Crew(
        agents=[
            market_research_agent,
            content_strategist_agent,
            channel_specialist_agent,
            campaign_planner_agent,
            budget_analyst_agent
        ],
        tasks=[
            market_research_task,
            content_strategy_task,
            channel_strategy_task,
            campaign_plan_task,
            budget_allocation_task
        ],
        verbose=True,
        process="sequential"  # Tasks execute in order, each building on previous outputs
    )

    print("Crew formed successfully!")
    print()
    print("=" * 80)
    print("Starting Marketing Strategy Development...")
    print("=" * 80)
    print()

    # Execute the crew
    try:
        result = crew.kickoff()
        
        print()
        print("=" * 80)
        print("✅ Marketing Strategy Development Completed Successfully!")
        print("=" * 80)
        print()

        # Save output to file
        output_dir = Path(__file__).parent
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = output_dir / f"marketing_strategy_{product_name.replace(' ', '_').lower()}_{timestamp}.txt"
        
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("MARKETING STRATEGY REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Product: {product_name}\n")
            f.write(f"Category: {product_category}\n")
            f.write(f"Target Audience: {target_audience}\n")
            f.write(f"Budget: ${total_budget:,.0f}\n")
            f.write(f"Timeline: {campaign_timeline}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("=" * 80 + "\n")
            f.write("COMPREHENSIVE MARKETING STRATEGY\n")
            f.write("=" * 80 + "\n\n")
            f.write(str(result))
            f.write("\n" + "=" * 80 + "\n")

        print(f"✅ Marketing strategy saved to: {output_filename}")
        print()
        print("📋 Strategy includes:")
        print("   • Market research and competitive analysis")
        print("   • Content strategy and messaging framework")
        print("   • Channel strategy and recommendations")
        print("   • Detailed campaign plan with timeline")
        print("   • Budget allocation and ROI projections")
        print()

    except Exception as e:
        print(f"\n❌ Error during crew execution: {str(e)}")
        print("\n🔍 Troubleshooting:")
        print("   1. Verify OPENAI_API_KEY is set in parent directory .env file")
        print("   2. Check API key is valid and has sufficient credits")
        print("   3. Verify internet connection")
        print()
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Allow command line arguments to override defaults
    import sys

    kwargs = {
        "product_name": "AI-Powered Task Manager",
        "product_category": "Productivity Software",
        "product_description": "An AI-powered task management application that helps teams organize, prioritize, and complete work more efficiently",
        "target_audience": "Small to medium-sized business teams and remote workers",
        "unique_value_proposition": "Intelligent task prioritization using AI, seamless team collaboration, and automated workflow optimization",
        "marketing_objectives": "Increase brand awareness, generate qualified leads, and drive product sign-ups",
        "campaign_timeline": "3 months (Q1 launch campaign)",
        "total_budget": 50000.0
    }

    # Parse command line arguments (optional)
    # Usage: python crewai_marketing_strategy.py [product_name] [category] [budget]
    if len(sys.argv) > 1:
        kwargs["product_name"] = sys.argv[1]
    if len(sys.argv) > 2:
        kwargs["product_category"] = sys.argv[2]
    if len(sys.argv) > 3:
        kwargs["total_budget"] = float(sys.argv[3])

    main(**kwargs)

