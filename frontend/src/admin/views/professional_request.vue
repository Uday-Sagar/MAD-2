<template>
    <div class="admin-layout">
        <AdminNavBar />
        <div class="admin-main-content">
            <h3><strong>Pending Service Professional Requests</strong></h3>
            <table class="table table-bordered">
                <thead class="table-light">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Service Type</th>
                        <th>Contact</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="professional in professionals" :key="professional.professional_id">
                        <td>{{ professional.professional_id }}</td>
                        <td>{{ professional.name }}</td>
                        <td>{{ professional.email }}</td>
                        <td>{{ professional.service_type }}</td>
                        <td>{{ professional.contact || 'N/A' }}</td>
                        <td>
                            <button class="btn btn-success btn-sm me-2" @click="approveProfessional(professional)">
                                Approve
                            </button>
                            <br/>
                            <button class="btn btn-danger btn-sm" @click="rejectProfessional(professional)">
                                Reject
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import AdminNavBar from '@/admin/components/navbar.vue'
import axios from 'axios'

export default {
name: "ProfessionalRequest",
components: { AdminNavBar },
data() {
    return {
        professionals: []
    }
},
mounted() {
    this.fetchPendingProfessionals();
},
methods: {
    async fetchPendingProfessionals() {
        try {
            const token = localStorage.getItem("token"); // Retrieve JWT token
            const response = await axios.get('http://127.0.0.1:7644/get_professional_approval', {
                headers: { Authorization: `Bearer ${token}` } // Include JWT in headers
            });

            if (response.data.success) {
                this.professionals = response.data.professionals;
            } else {
                console.error("Failed to fetch professionals", response.data.message);
            }
        } catch (error) {
            console.error("Error fetching professionals:", error);
        }
    },

    async approveProfessional(professional) {
        const confirmApproval = window.confirm(`Are you sure you want to approve ${professional.name}?`);
        if (!confirmApproval) return;
        try {
            const token = localStorage.getItem("token"); 
            const response = await axios.put(`http://127.0.0.1:7644/approve_professional/${professional.professional_id}`,
                { status: true },
                {
                    headers: { 
                        Authorization: `Bearer ${token}`, // Include JWT in headers
                        'Content-Type': 'application/json' 
                    }
                }
            );

            if (response.data.success) {
                alert(`${professional.name} has been approved.`);
                this.professionals = this.professionals.filter(p => p.professional_id !== professional.professional_id);
            } else {
                console.error("Failed to approve professional:", response.data.message);
            }
        } catch (error) {
            console.error("Error approving professional:", error);
        }
    },

    rejectProfessional(professional) {
        const confirmRejection = window.confirm(`Are you sure you want to reject ${professional.name}?`);
        if (!confirmRejection) return;

        alert(`${professional.name} has been rejected.`);
        this.professionals = this.professionals.filter(p => p.professional_id !== professional.professional_id);
    },
}
};
</script>


<style scoped>
.table {
    width: 100%;
    margin-top: 20px;
    border-collapse: collapse;
}

.table th, .table td {
    padding: 10px;
    border: 1px solid #ddd;
    text-align: left;
}

.btn {
    cursor: pointer;
    padding: 5px 10px;
}
</style>
