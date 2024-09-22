import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [items, setItems] = useState([]);
    const [newItem, setNewItem] = useState('');
    const [editItem, setEditItem] = useState({ id: null, name: '' });
    const [isEditing, setIsEditing] = useState(false);

    useEffect(() => {
        fetchItems();
    }, []);

    const fetchItems = async () => {
        try {
            const response = await axios.get('http://localhost:5000/items');
            setItems(response.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const addItem = async () => {
        if (!newItem) return;
        try {
            await axios.post('http://localhost:5000/items', { name: newItem });
            setNewItem('');
            fetchItems();
        } catch (error) {
            console.error('Error adding item:', error);
        }
    };

    const updateItem = async () => {
        if (!editItem.name) return;
        try {
            await axios.put(`http://localhost:5000/items/${editItem.id}`, { name: editItem.name });
            setEditItem({ id: null, name: '' });
            setIsEditing(false);
            fetchItems();
        } catch (error) {
            console.error('Error updating item:', error);
        }
    };

    const deleteItem = async (id) => {
        try {
            await axios.delete(`http://localhost:5000/items/${id}`);
            fetchItems();
        } catch (error) {
            console.error('Error deleting item:', error);
        }
    };

    return (
        <div className="app-container">
            <h1>Danh Sách Items</h1>
            <div className="input-group">
                <input
                    type="text"
                    value={newItem}
                    onChange={(e) => setNewItem(e.target.value)}
                    placeholder="Thêm item mới"
                />
                <button onClick={addItem}>Thêm</button>
            </div>

            {isEditing && (
                <div className="edit-group">
                    <input
                        type="text"
                        value={editItem.name}
                        onChange={(e) => setEditItem({ ...editItem, name: e.target.value })}
                        placeholder="Tên item cần sửa"
                    />
                    <button onClick={updateItem}>Cập Nhật</button>
                </div>
            )}

            <ul className="item-list">
                {items.map(item => (
                    <li key={item.id}>
                        {item.name}
                        <div className="button-group">
                            <button onClick={() => {
                                setEditItem({ id: item.id, name: item.name });
                                setIsEditing(true);
                            }}>Sửa</button>
                            <button onClick={() => deleteItem(item.id)}>Xóa</button>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;