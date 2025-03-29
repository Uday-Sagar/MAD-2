<template>
    <div class="admin-layout">
        <AdminNavBar />
        <div class="admin-main-content">
            <div class="header">
                <h2>Edit Service</h2>
            </div>

            <form @submit.prevent="updateService" class="service-form">
                <label for="type">Service Type:</label>
                <input type="text" id="type" v-model="service.Service_type" required>

                <label for="price">Price Range:</label>
                <input type="text" id="price" v-model="service.Price_range" required>

                <label for="duration">Duration:</label>
                <input type="text" id="duration" v-model="service.Duration" required>

                <label for="description">Description:</label>
                <textarea id="description" v-model="service.Description" required></textarea>

                <button type="submit" class="submit-button">Update Service</button>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import AdminNavBar from '@/admin/components/navbar.vue';

export default {
    name: "EditService",
    components: { AdminNavBar },
    data() {
        return {
            service: {
                Service_type: '',
                Price_range: '',
                Duration: '',
                Description: ''
            }
        };
    },
    methods: {
        async fetchService() {
            try {
                const serviceId = this.$route.params.id;
                const token = localStorage.getItem("token");
                const response = await axios.get(`http://127.0.0.1:7644/edit_service/${serviceId}`, {
                    headers: { Authorization: `Bearer ${token}` } });
                if (response.data.success) {
                    this.service = response.data.service;
                } else {
                    console.error("Failed to fetch service:", response.data.message);
                }
            } catch (error) {
                console.error("Error fetching service:", error);
            }
        },
        async updateService() {
            try {
                const serviceId = this.$route.params.id;
                const token = localStorage.getItem("token");
                const response = await axios.put(`http://127.0.0.1:7644/update_service/${serviceId}`, 
                    this.service,
                    {
                        headers: { Authorization: `Bearer ${token}` } // Include token
                    });

                if (response.data.success) {
                    alert('Service updated successfully');
                    this.$router.push(`/manage_services`);
                } else {
                    console.error("Failed to update service:", response.data.message);
                }
            } catch (error) {
                console.error("Error updating service:", error);
            }
        }
    },
    mounted() {
        this.fetchService();
    }
};
</script>

<style scoped>
.service-form {
    display: flex;
    flex-direction: column;
    width: 50%;
    margin: 20px auto;
}

.service-form label {
    margin-top: 10px;
    font-weight: bold;
}

.service-form input, .service-form textarea {
    padding: 8px;
    margin-top: 5px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
}

.service-form textarea {
    resize: vertical;
}

.submit-button {
    margin-top: 15px;
    background-color: #da99e7;
    color: black;
    border: none;
    padding: 10px 16px;
    font-size: 16px;
    border-radius: 5px;
    cursor: pointer;
}

.submit-button:hover {
    background-color: #0056b3;
}
</style>
