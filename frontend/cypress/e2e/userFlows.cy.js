describe('Key User Flows', () => {
  beforeEach(() => {
    // Reset application state before each test
    cy.visit('/');
  });
  
  it('logs in, submits an idea, drags a card in Kanban, and logs out', () => {
    // 1. Visit homepage and go to login
    cy.contains('Login').click();

    // 2. Perform login
    cy.get('input[name="email"]').type('your-test-user@example.com');
    cy.get('input[name="password"]').type('password123');
    cy.get('button[type="submit"]').click();
    cy.contains('Logout');

    // 3. Navigate to New Idea form, submit an idea
    cy.contains('New Idea').click();
    cy.get('input[name="title"]').type('Cypress Test Idea');
    cy.get('textarea[name="description"]').type('This idea was submitted via Cypress test.');
    cy.get('button[type="submit"]').click();
    cy.contains('Idea submitted successfully!');

    // 4. Navigate to Kanban and drag a card
    cy.contains('Kanban').click();
    cy.get('.kanban-card').first()
      .trigger('mousedown', { which: 1 });
    cy.get('.kanban-column').eq(1)
      .trigger('mousemove')
      .trigger('mouseup', { force: true });
    
    // Assert card was moved successfully
    cy.get('.kanban-column').eq(1).find('.kanban-card').should('exist');

    // 5. Logout
    cy.contains('Logout').click();
    cy.contains('Login');
  });
  
  it('fails login with invalid credentials and shows error message', () => {
    // Test login failure scenario
    cy.contains('Login').click();
    cy.get('input[name="email"]').type('invalid@example.com');
    cy.get('input[name="password"]').type('wrongpassword');
    cy.get('button[type="submit"]').click();
    
    // Check for error toast
    cy.contains('Login failed').should('be.visible');
    
    // Verify we're still on login page
    cy.url().should('include', '/login');
  });
  
  it('navigates to SOP viewer/uploader and interacts with it', () => {
    // Login first
    cy.contains('Login').click();
    cy.get('input[name="email"]').type('your-test-user@example.com');
    cy.get('input[name="password"]').type('password123');
    cy.get('button[type="submit"]').click();
    
    // Go to SOP page
    cy.contains('SOPs').click();
    cy.url().should('include', '/sop');
    
    // Test file upload if your test environment supports it
    // This is a simplified version; actual implementation may vary
    cy.get('input[type="file"]').should('exist');
    
    // Verify SOP table exists
    cy.get('.sop-table').should('exist');
  });
  
  it('visits KPI dashboard and checks charts are rendered', () => {
    // Login first
    cy.contains('Login').click();
    cy.get('input[name="email"]').type('your-test-user@example.com');
    cy.get('input[name="password"]').type('password123');
    cy.get('button[type="submit"]').click();
    
    // Go to KPI dashboard
    cy.contains('KPI').click();
    cy.url().should('include', '/kpi');
    
    // Check charts are rendered
    cy.get('.recharts-surface').should('exist');
    
    // Test toggle between chart views
    cy.contains('Financial Metrics').click();
    cy.get('.financial-metrics-container').should('be.visible');
    
    cy.contains('Project Metrics').click();
    cy.get('.project-metrics-container').should('be.visible');
  });
});
