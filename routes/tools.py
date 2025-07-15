from flask import Blueprint, render_template, jsonify, request

# Create a Blueprint for tools
tools_bp = Blueprint('tools', __name__)

# Sample tools data (consider moving to a database later)
TOOLS = [
    {
        'id': 'autohired',
        'name': 'AutoHired',
        'description': 'AI-powered resume + job application bot',
        'category': 'Productivity',
        'status': 'Active'
    },
    {
        'id': 'organiserpro',
        'name': 'OrganiserPro',
        'description': 'CLI-based file management tool',
        'category': 'Developer Tools',
        'status': 'Active',
        'download': 'organiserpro.zip'
    },
    {
        'id': 'shelltasker',
        'name': 'ShellTasker',
        'description': 'Custom script automation via reusable CLI commands',
        'category': 'Developer Tools',
        'status': 'Active'
    },
    {
        'id': 'quickdeploy',
        'name': 'QuickDeploy CLI',
        'description': 'One-command full-stack deploy to Vercel/Netlify',
        'category': 'DevOps',
        'status': 'Beta'
    }
]

@tools_bp.route('/')
def list_tools():
    """List all available tools"""
    return render_template('tools.html', tools=TOOLS)

@tools_bp.route('/<tool_id>')
def tool_detail(tool_id):
    """Show details for a specific tool"""
    tool = next((t for t in TOOLS if t['id'] == tool_id), None)
    if not tool:
        return render_template('404.html'), 404
    return render_template('tool_detail.html', tool=tool)

# API Endpoints
@tools_bp.route('/api/tools', methods=['GET'])
def api_list_tools():
    """API endpoint to list all tools"""
    return jsonify(TOOLS)

@tools_bp.route('/api/tools/<tool_id>', methods=['GET'])
def api_get_tool(tool_id):
    """API endpoint to get a specific tool"""
    tool = next((t for t in TOOLS if t['id'] == tool_id), None)
    if not tool:
        return jsonify({'error': 'Tool not found'}), 404
    return jsonify(tool)
