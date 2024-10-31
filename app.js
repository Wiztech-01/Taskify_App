import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState('');

  useEffect(() => {
    // Fetch tasks from the backend
    axios.get('http://127.0.0.1:5000/api/tasks')
      .then((response) => setTasks(response.data))
      .catch((error) => console.error("There was an error fetching tasks:", error));
  }, []);

  const handleAddTask = () => {
    axios.post('http://127.0.0.1:5000/api/tasks', { id: tasks.length + 1, task: newTask, completed: false })
      .then((response) => {
        setTasks([...tasks, response.data]);
        setNewTask('');
      })
      .catch((error) => console.error("There was an error adding the task:", error));
  };

  return (
    <div className="App">
      <h1>Taskify</h1>
      <input
        type="text"
        value={newTask}
        onChange={(e) => setNewTask(e.target.value)}
        placeholder="Add a new task"
      />
      <button onClick={handleAddTask}>Add Task</button>
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>{task.task}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
