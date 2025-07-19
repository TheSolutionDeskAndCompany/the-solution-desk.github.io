#!/usr/bin/env python3
"""
Check test coverage thresholds and fail if not met.
"""
import os
import sys
import json
import xml.etree.ElementTree as ET
from typing import Dict, Optional, Tuple

def parse_cobertura_coverage(coverage_file: str) -> Dict[str, float]:
    """Parse Cobertura XML coverage file and return coverage metrics."""
    try:
        tree = ET.parse(coverage_file)
        root = tree.getroot()
        
        # Get coverage metrics from the XML
        coverage = root.attrib
        metrics = {
            'line_rate': float(coverage.get('line-rate', 0)) * 100,
            'branch_rate': float(coverage.get('branch-rate', 0)) * 100,
            'lines_covered': int(coverage.get('lines-covered', 0)),
            'lines_valid': int(coverage.get('lines-valid', 0)),
            'branches_covered': int(coverage.get('branches-covered', 0)),
            'branches_valid': int(coverage.get('branches-valid', 0))
        }
        return metrics
    except (ET.ParseError, FileNotFoundError) as e:
        print(f"Error parsing coverage file {coverage_file}: {e}")
        return {}

def parse_lcov_coverage(lcov_file: str) -> Dict[str, float]:
    """Parse LCOV coverage file and return coverage metrics."""
    try:
        with open(lcov_file, 'r') as f:
            lcov_data = f.read()
        
        lines = lcov_data.split('\n')
        metrics = {
            'lines_found': 0,
            'lines_hit': 0,
            'branches_found': 0,
            'branches_hit': 0
        }
        
        for line in lines:
            if line.startswith('LF:'):
                metrics['lines_found'] = int(line.split(':')[1])
            elif line.startswith('LH:'):
                metrics['lines_hit'] = int(line.split(':')[1])
            elif line.startswith('BRF:'):
                metrics['branches_found'] = int(line.split(':')[1])
            elif line.startswith('BRH:'):
                metrics['branches_hit'] = int(line.split(':')[1])
        
        # Calculate percentages
        metrics['line_rate'] = (metrics['lines_hit'] / metrics['lines_found'] * 100) if metrics['lines_found'] > 0 else 0
        metrics['branch_rate'] = (metrics['branches_hit'] / metrics['branches_found'] * 100) if metrics['branches_found'] > 0 else 0
        
        return metrics
    except FileNotFoundError as e:
        print(f"Error reading LCOV file {lcov_file}: {e}")
        return {}

def check_coverage_thresholds(
    backend_coverage: Dict[str, float],
    frontend_coverage: Dict[str, float],
    min_line_coverage: float = 80.0,
    min_branch_coverage: float = 75.0
) -> Tuple[bool, str]:
    """Check if coverage meets the minimum thresholds."""
    errors = []
    
    # Check backend coverage
    if not backend_coverage:
        errors.append("Backend coverage data not found")
    else:
        if backend_coverage['line_rate'] < min_line_coverage:
            errors.append(
                f"Backend line coverage is {backend_coverage['line_rate']:.2f}% "
                f"(minimum required: {min_line_coverage}%)"
            )
        if backend_coverage['branch_rate'] < min_branch_coverage:
            errors.append(
                f"Backend branch coverage is {backend_coverage['branch_rate']:.2f}% "
                f"(minimum required: {min_branch_coverage}%)"
            )
    
    # Check frontend coverage
    if not frontend_coverage:
        errors.append("Frontend coverage data not found")
    else:
        if frontend_coverage['line_rate'] < min_line_coverage:
            errors.append(
                f"Frontend line coverage is {frontend_coverage['line_rate']:.2f}% "
                f"(minimum required: {min_line_coverage}%)"
            )
        if frontend_coverage['branch_rate'] < min_branch_coverage:
            errors.append(
                f"Frontend branch coverage is {frontend_coverage['branch_rate']:.2f}% "
                f"(minimum required: {min_branch_coverage}%)"
            )
    
    if errors:
        return False, "\n".join(["Coverage thresholds not met:"] + [f"- {error}" for error in errors])
    
    return True, "All coverage thresholds met"

def main():
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Check test coverage thresholds')
    parser.add_argument('--backend-coverage', default='coverage.xml',
                        help='Path to backend coverage file (Cobertura XML)')
    parser.add_argument('--frontend-coverage', default='frontend/coverage/lcov.info',
                        help='Path to frontend coverage file (LCOV)')
    parser.add_argument('--min-line-coverage', type=float, default=80.0,
                        help='Minimum line coverage percentage (default: 80)')
    parser.add_argument('--min-branch-coverage', type=float, default=75.0,
                        help='Minimum branch coverage percentage (default: 75)')
    args = parser.parse_args()
    
    # Parse coverage files
    backend_metrics = parse_cobertura_coverage(args.backend_coverage)
    frontend_metrics = parse_lcov_coverage(args.frontend_coverage)
    
    # Check thresholds
    success, message = check_coverage_thresholds(
        backend_metrics,
        frontend_metrics,
        args.min_line_coverage,
        args.min_branch_coverage
    )
    
    print(message)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
