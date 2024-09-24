import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';  // Nhập tệp CSS

function App() {
  const [users, setUsers] = useState([]);
  const [name, setName] = useState('');
  const [age, setAge] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const result = await axios.get('http://localhost:5000/api/users');
    setUsers(result.data);
  };

  const addUser = async () => {
    await axios.post('http://localhost:5000/api/users', { name, age: parseInt(age) });
    fetchData();  
    setName('');
    setAge('');
  };

  const deleteUser = async (userId) => {
    await axios.delete(`http://localhost:5000/api/users/${userId}`);
    fetchData();  
  };

  return (
    <div className="container">
      <h1>User List</h1>
      <ul>
        {users.map(user => (
          <li key={user[0]}>
            {user[1]} - {user[2]} 
            <button onClick={() => deleteUser(user[0])}>Delete</button>
          </li>
        ))}
      </ul>
      <h2>Add User</h2>
      <div className="add-user-container">
        <input 
          type="text" 
          placeholder="Name" 
          value={name} 
          onChange={(e) => setName(e.target.value)} 
        />
        <input 
          type="number" 
          placeholder="Age" 
          value={age} 
          onChange={(e) => setAge(e.target.value)} 
        />
        <button onClick={addUser}>Add User</button>
      </div>
    </div>
  );
}

export default App;