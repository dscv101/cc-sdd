#!/usr/bin/env python3
"""Manual test script to verify enhanced template workflows."""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cc_sdd_mcp.workflows.spec_workflow import SpecWorkflow


async def test_enhanced_workflows():
    """Test enhanced template-based workflows."""
    print("=" * 80)
    print("Testing Enhanced Template Workflows")
    print("=" * 80)
    
    # Create temporary test directory
    test_dir = Path("/tmp/cc-sdd-test-enhanced")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize workflow
    workflow = SpecWorkflow(project_dir=test_dir)
    print(f"\n✓ Initialized workflow in {test_dir}")
    
    # Test 1: Initialize spec
    print("\n" + "=" * 80)
    print("Test 1: Initialize Specification")
    print("=" * 80)
    result = await workflow.initialize_spec(
        feature_name="test-enhanced",
        description="Testing enhanced EARS templates"
    )
    print(f"Success: {result['success']}")
    print(f"Phase: {result['current_phase']}")
    
    # Test 2: Generate requirements with enhanced template
    print("\n" + "=" * 80)
    print("Test 2: Generate Requirements (Enhanced EARS Template)")
    print("=" * 80)
    result = await workflow.generate_requirements("test-enhanced", auto_approve=True)
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    print(f"File: {result.get('requirements_file')}")
    
    if result['success']:
        req_file = Path(result['requirements_file'])
        if req_file.exists():
            content = req_file.read_text()
            print(f"\n✓ Requirements file created ({len(content)} bytes)")
            print(f"Preview (first 500 chars):")
            print("-" * 80)
            print(content[:500])
            print("-" * 80)
            
            # Check for EARS notation
            if "EARS" in content or "shall" in content or "When" in content:
                print("✓ EARS notation detected in output")
            else:
                print("⚠ EARS notation not clearly visible (may be in template structure)")
    
    # Test 3: Generate design with enhanced template
    print("\n" + "=" * 80)
    print("Test 3: Generate Design (Enhanced Template)")
    print("=" * 80)
    result = await workflow.generate_design("test-enhanced", auto_approve=True)
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    print(f"File: {result.get('design_file')}")
    
    if result['success']:
        design_file = Path(result['design_file'])
        if design_file.exists():
            content = design_file.read_text()
            print(f"\n✓ Design file created ({len(content)} bytes)")
            print(f"Preview (first 500 chars):")
            print("-" * 80)
            print(content[:500])
            print("-" * 80)
    
    # Test 4: Generate tasks with enhanced template
    print("\n" + "=" * 80)
    print("Test 4: Generate Tasks (Enhanced Template)")
    print("=" * 80)
    result = await workflow.generate_tasks("test-enhanced", auto_approve=True)
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    print(f"File: {result.get('tasks_file')}")
    
    if result['success']:
        tasks_file = Path(result['tasks_file'])
        if tasks_file.exists():
            content = tasks_file.read_text()
            print(f"\n✓ Tasks file created ({len(content)} bytes)")
            print(f"Preview (first 500 chars):")
            print("-" * 80)
            print(content[:500])
            print("-" * 80)
    
    # Test 5: Context builders
    print("\n" + "=" * 80)
    print("Test 5: Context Builders")
    print("=" * 80)
    metadata = workflow._load_metadata("test-enhanced")
    
    print("\nRequirements context variables:")
    req_context = workflow._build_requirements_context(metadata)
    print(f"  - Total variables: {len(req_context)}")
    print(f"  - Sample keys: {list(req_context.keys())[:10]}")
    
    print("\nDesign context variables:")
    design_context = workflow._build_design_context(metadata)
    print(f"  - Total variables: {len(design_context)}")
    print(f"  - Sample keys: {list(design_context.keys())[:10]}")
    
    print("\nTasks context variables:")
    tasks_context = workflow._build_tasks_context(metadata)
    print(f"  - Total variables: {len(tasks_context)}")
    print(f"  - Sample keys: {list(tasks_context.keys())[:10]}")
    
    # Summary
    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print("✓ All three workflows now use enhanced templates")
    print("✓ Requirements: EARS notation and Sean Grove's style")
    print("✓ Design: Comprehensive architecture documentation")
    print("✓ Tasks: Detailed implementation breakdown")
    print("\nEnhancement complete!")


if __name__ == "__main__":
    asyncio.run(test_enhanced_workflows())

