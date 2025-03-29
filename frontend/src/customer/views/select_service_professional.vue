<template>
    <div class="cust-layout">
        <CustomerNavBar />
        <div class="cust-main-content">
            <h2><strong>{{ serviceType }}</strong></h2>
            <h3>Select a service professional for the work consultation.</h3>
            
            <table v-if="professionals.length" class="styled-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Experience</th>
                        <th>City</th>
                        <th>Locality</th>
                        <th>Contact</th>
                        <th>Description</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="professional in professionals" :key="professional.id">
                        <td>{{ professional.id }}</td>
                        <td>{{ professional.name }}</td>
                        <td>{{ professional.email }}</td>
                        <td>{{ professional.experience }}</td>
                        <td>{{ professional.city }}</td>
                        <td>{{ professional.locality }}</td>
                        <td>{{ professional.contact || 'N/A' }}</td>
                        <td>{{ professional.description }}</td>
                        <td>
                            <button class="request-btn" @click="sendRequest(professional.id)">Send Request</button>
                        </td>
                    </tr>
                </tbody>
            </table>
            
            <p v-else><strong>No service professionals available for this service type.</strong></p>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import CustomerNavBar from '@/customer/components/navbar.vue';

export default {
    name: 'SelectServiceProfessional',
    components: { CustomerNavBar },
    props: ["serviceType"],
    data() {
        return {
            professionals: [],
            user_id: this.$route.query.user_id,
        };
    },
    mounted() {
        this.fetchProfessionals();
    },
    methods: {
        async fetchProfessionals() {
            try {
                const response = await axios.get('http://127.0.0.1:7644/get_service_professionals_by_type', {
                    params: { serviceType: this.serviceType }
                });
                if (response.data.success) {
                    this.professionals = response.data.professionals;
                } else {
                    console.error('Failed to fetch professionals:', response.data.message);
                }
            } catch (error) {
                console.error('Error fetching professionals:', error);
            }
        },
        sendRequest(professionalId) {
        this.$router.push({ 
            path: '/create_service_request', 
            query: { 
                professionalId, 
                serviceType: this.$route.query.serviceType,
                user_id: this.user_id 
            } 
        });
    }
    }
};
</script>

<style scoped>
.styled-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    font-size: 16px;
    text-align: left;
}

.styled-table th, .styled-table td {
    padding: 12px;
    border: 1px solid #ddd;
}

.styled-table thead {
    background-color: #f4f4f4;
    font-weight: bold;
}

.styled-table tbody tr:nth-child(even) {
    background-color: #f9f9f9;
}

.styled-table tbody tr:hover {
    background-color: #f1f1f1;
}
.request-btn {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 8px 12px;
    cursor: pointer;
    border-radius: 4px;
}

.request-btn:hover {
    background-color: #0056b3;
}
</style>
