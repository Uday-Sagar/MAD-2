<template>
    <div class="admin-layout">
        <AdminNavBar />
        <div class="admin-main-content">
            <div class="header">
                <h2>Add New Service</h2>
            </div>

            <form @submit.prevent="addService" class="service-form">
                <label for="type">Service Type:</label>
                <input type="text" id="type" v-model="serviceType" required>

                <label for="price">Price Range:</label>
                <input type="text" id="price" v-model="priceRange" required>

                <label for="duration">Duration:</label>
                <input type="text" id="duration" v-model="duration" required>

                <label for="description">Description:</label>
                <textarea id="description" v-model="description" required></textarea>

                <button type="submit" class="submit-button">Add Service</button>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import AdminNavBar from '@/admin/components/navbar.vue';

export default {
    name: "AddService",
    components: { AdminNavBar },
    data() {
        return {
            serviceType: '',
            priceRange: '',
            duration: '',
            description: ''
        };
    },
    methods: {
        async addService() {
            try {
                const token = localStorage.getItem("token"); 
                const response = await axios.post("http://127.0.0.1:7644/add_service",
                    {
                        service_type: this.serviceType,
                        price_range: this.priceRange,
                        duration: this.duration,
                        description: this.description,
                    },
                    {
                        headers: { Authorization: `Bearer ${token}` },
                    }
                );
                
                if (response.data.success) {
                    alert("New service type added");
                    this.$router.push(`/manage_services`);
                } else {
                    console.error("Failed to add service:", response.data.message);
                }
            } catch (error) {
                console.error("Error adding service:", error);
            }
        }
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
