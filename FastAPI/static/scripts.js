async function loadUsers() {
    try {
        const response = await fetch('/api/v1/users');
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const users = await response.json();
        const container = document.getElementById('userBody');

        // Limpiamos el contenedor antes de agregar filas
        container.innerHTML = '';

        users.forEach(u => {
            const row = document.createElement('tr');

            const nameCell = document.createElement('td');
            nameCell.innerHTML = `<strong>${u.first_name} ${u.last_name}</strong>`;
            row.appendChild(nameCell);

            const genderCell = document.createElement('td');
            genderCell.textContent = u.gender;
            row.appendChild(genderCell);

            const rolesCell = document.createElement('td');
            rolesCell.textContent = u.roles.join(', ');
            row.appendChild(rolesCell);

            container.appendChild(row);
        });

    } catch (error) {
        console.error('Error cargando usuarios:', error);
        alert('No se pudieron cargar los usuarios. Revisa la consola.');
    }
}

// Event listener para botón de refrescar
const refreshBtn = document.getElementById('refresh-btn');
if (refreshBtn) {
    refreshBtn.addEventListener('click', loadUsers);
}

// Cargar usuarios al inicio
document.addEventListener('DOMContentLoaded', loadUsers);

// Event listener para formulario
const userForm = document.getElementById('userForm');
if (userForm) {
    userForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const userData = {
            first_name: document.getElementById('firstName').value.trim(),
            last_name: document.getElementById('lastName').value.trim(),
            gender: document.getElementById('gender').value,
            roles: [document.getElementById('role').value]
        };

        try {
            const response = await fetch('/api/v1/users', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData)
            });

            if (response.ok) {
                userForm.reset();
                loadUsers();
            } else {
                const errorMsg = await response.text();
                alert(`Error al guardar el usuario: ${errorMsg}`);
            }
        } catch (error) {
            console.error('Error al guardar usuario:', error);
            alert('Ocurrió un error al guardar el usuario.');
        }
    });
}
