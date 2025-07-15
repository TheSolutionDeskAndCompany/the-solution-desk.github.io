import React, { useState, useEffect } from 'react';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import './ProjectKanbanBoard.css';

// This is a workaround for react-beautiful-dnd not working with React 19 and StrictMode
// See: https://github.com/atlassian/react-beautiful-dnd/issues/2399
const useUnsafeStrictModePatch = () => {
  useEffect(() => {
    // Hack for react-beautiful-dnd to work with React 19
    const originalConsoleError = console.error;
    console.error = (...args) => {
      if (
        typeof args[0] === 'string' &&
        args[0].includes('findDOMNode is deprecated in StrictMode')
      ) {
        return;
      }
      originalConsoleError(...args);
    };

    return () => {
      console.error = originalConsoleError;
    };
  }, []);
};

const initialData = {
  toDo: [
    { id: '1', content: 'Research competitor products', priority: 'high' },
    { id: '2', content: 'Create initial wireframes', priority: 'medium' },
    { id: '5', content: 'Document user stories', priority: 'medium' },
  ],
  inProgress: [
    { id: '3', content: 'Design landing page', priority: 'high' },
    { id: '6', content: 'Setup CI/CD pipeline', priority: 'low' },
  ],
  done: [
    { id: '4', content: 'Project kickoff meeting', priority: 'high' },
    { id: '7', content: 'Domain name registration', priority: 'low' },
  ],
};

export default function ProjectKanbanBoard() {
  // Apply the workaround for React 19 compatibility
  useUnsafeStrictModePatch();
  
  const [data, setData] = useState(initialData);

  const handleDragEnd = (result) => {
    const { destination, source } = result;
    
    // If dropped outside a droppable area or in the same position
    if (!destination || 
        (destination.droppableId === source.droppableId && 
         destination.index === source.index)) {
      return;
    }

    // Make copies of the source and destination lists
    const sourceList = [...data[source.droppableId]];
    const destList = source.droppableId === destination.droppableId 
      ? sourceList 
      : [...data[destination.droppableId]];

    // Remove the dragged item from the source list
    const [removed] = sourceList.splice(source.index, 1);
    
    // Insert the item into the destination list
    destList.splice(destination.index, 0, removed);

    // Create new state with updated lists
    const newData = {...data};
    
    newData[source.droppableId] = sourceList;
    if (source.droppableId !== destination.droppableId) {
      newData[destination.droppableId] = destList;
    }

    setData(newData);
  };

  const getColumnTitle = (id) => {
    const titles = {
      'toDo': 'To Do',
      'inProgress': 'In Progress',
      'done': 'Done'
    };
    return titles[id] || id;
  };

  const getPriorityClass = (priority) => {
    return `priority-${priority || 'default'}`;
  };

  return (
    <div className="kanban-container cyberpunk-theme">
      <h1>Project Kanban Board</h1>
      <div className="kanban-info">
        <p>Drag and drop tasks between columns to update their status.</p>
      </div>
      
      <DragDropContext onDragEnd={handleDragEnd}>
        <div className="kanban-board">
          {['toDo', 'inProgress', 'done'].map((columnId) => (
            <div key={columnId} className="kanban-column-wrapper">
              <h2 className="column-title">{getColumnTitle(columnId)}</h2>
              <Droppable droppableId={columnId}>
                {(provided, snapshot) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.droppableProps}
                    className={`kanban-column ${snapshot.isDraggingOver ? 'dragging-over' : ''}`}
                  >
                    {data[columnId].map((task, index) => (
                      <Draggable key={task.id} draggableId={task.id} index={index}>
                        {(provided, snapshot) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            className={`kanban-card ${getPriorityClass(task.priority)} ${snapshot.isDragging ? 'dragging' : ''}`}
                          >
                            <div className="card-content">{task.content}</div>
                            <div className="card-priority">{task.priority}</div>
                          </div>
                        )}
                      </Draggable>
                    ))}
                    {provided.placeholder}
                  </div>
                )}
              </Droppable>
            </div>
          ))}
        </div>
      </DragDropContext>
    </div>
  );
}
