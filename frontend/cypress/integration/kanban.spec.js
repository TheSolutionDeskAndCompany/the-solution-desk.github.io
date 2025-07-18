describe('Kanban Board', () => {
  beforeEach(() => {
    // Visit the Kanban board page
    cy.visit('/kanban');
    // Wait for the board to be fully loaded
    cy.get('[data-cy=kanban-board]').should('be.visible');
  });

  it('displays three columns: To Do, In Progress, and Done', () => {
    // Check that all three columns are visible
    cy.get('[data-cy^=column-]').should('have.length', 3);
    
    // Check the column titles
    cy.contains('h2', 'To Do').should('be.visible');
    cy.contains('h2', 'In Progress').should('be.visible');
    cy.contains('h2', 'Done').should('be.visible');
  });

  it('allows dragging a task from To Do to In Progress', () => {
    // Get the first task in the To Do column
    cy.get('[data-cy=column-todo] [data-cy^=card-]').first().as('taskToMove');
    
    // Get the task's text
    cy.get('@taskToMove').invoke('text').then((taskText) => {
      // Drag the task to the In Progress column
      cy.get('@taskToMove').drag('[data-cy=column-inprogress]');
      
      // Verify the task is now in the In Progress column
      cy.get('[data-cy=column-inprogress]').should('contain.text', taskText.trim());
      
      // Verify the task is no longer in the To Do column (or is still there but with position updated)
      cy.get('[data-cy=column-todo]').should('not.contain', taskText.trim());
    });
  });

  it('allows reordering tasks within a column', () => {
    // Get the first and second tasks in the To Do column
    cy.get('[data-cy=column-todo] [data-cy^=card-]').first().as('firstTask');
    cy.get('[data-cy=column-todo] [data-cy^=card-]').eq(1).as('secondTask');
    
    // Get the text of the first task
    cy.get('@firstTask').invoke('text').then((firstTaskText) => {
      // Drag the first task below the second task
      cy.get('@firstTask').drag('@secondTask', { position: 'bottom' });
      
      // The first task should now be after the second task
      cy.get('[data-cy=column-todo] [data-cy^=card-]').eq(1).should('contain.text', firstTaskText);
    });
  });

  it('returns task to original position when dropped outside a column', () => {
    // Get the first task in the To Do column
    cy.get('[data-cy=column-todo] [data-cy^=card-]').first().as('taskToMove');
    
    // Get the initial position of the task
    cy.get('@taskToMove').then(($el) => {
      const initialPosition = $el.position();
      
      // Drag the task to a position outside any column
      cy.get('@taskToMove')
        .trigger('mousedown', { which: 1, force: true })
        .trigger('mousemove', { clientX: 10, clientY: 10, force: true })
        .trigger('mouseup', { force: true });
      
      // The task should still be in the same position
      cy.get('@taskToMove').should(($el) => {
        const newPosition = $el.position();
        expect(newPosition.top).to.be.closeTo(initialPosition.top, 5);
        expect(newPosition.left).to.be.closeTo(initialPosition.left, 5);
      });
    });
  });
});
