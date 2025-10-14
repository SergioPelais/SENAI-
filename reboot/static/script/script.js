let users = [];




function createUser(user) {
  users.push(user);
  return user;
}




function getUserById(id) {
  return users.find(u => u.id === id);
}




function updateUser(id, newData) {
  const index = users.findIndex(u => u.id === id);
  if (index === -1) return null;
  users[index] = { ...users[index], ...newData };
  return users[index];
}




function deleteUser(id) {
  const index = users.findIndex(u => u.id === id);
  if (index === -1) return false;
  users.splice(index, 1);
  return true;
}




function resetUsers() {
  users = [];
  if(!users.length){
    return true
  }
  return false
}