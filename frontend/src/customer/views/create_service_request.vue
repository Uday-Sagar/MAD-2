<template>
    <div class="cust-layout">
        <CustomerNavBar />
        <div class="cust-main-content">
            <h3>Fill in the details to proceed with your service request.</h3>

            <div class="service-details">
                <p><strong>Service Type:</strong> {{ serviceType }}</p>
                <p><strong>Professional Name:</strong> {{ professional.name }}</p>
                <p><strong>Professional Email:</strong> {{ professional.email }}</p>
            </div>

            <form @submit.prevent="submitRequest" class="request-form">
                <label for="location">Location:</label>
                <input type="text" id="location" v-model="location" required>

                <label for="start_date">Start Date:</label>
                <input type="date" id="start_date" v-model="startDate" required>

                <label for="end_date">End Date:</label>
                <input type="date" id="end_date" v-model="endDate">

                <button type="submit" class="submit-btn">Submit Request</button>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import CustomerNavBar from '@/customer/components/navbar.vue';

export default {
    name: 'CreateServiceRequest',
    components: { CustomerNavBar },
    data() {
        return {
            serviceType: this.$route.query.serviceType,
            professionalId: this.$route.query.professionalId,
            customerId: this.$route.params.user_id || this.$route.query.user_id,
            professional: {},
            location: '',
            startDate: '',
            endDate: ''
        };
    },
    mounted() {
        this.fetchProfessionalDetails();
    },
    methods: {
        async fetchProfessionalDetails() {
            try {
                const response = await axios.get(`http://127.0.0.1:7644/get_professional_by_id`, {
                    params: { professionalId: this.professionalId }
                });
                if (response.data.success) {
                    this.professional = response.data.professional;
                } else {
                    console.error('Failed to fetch professional:', response.data.message);
                }
            } catch (error) {
                console.error('Error fetching professional details:', error);
            }
        },
        async submitRequest() {
            try {
                const requestData = {
                    customerId: this.customerId, 
                    serviceType: this.serviceType,
                    professionalId: this.professionalId,
                    location: this.location,
                    startDate: this.startDate,
                    endDate: this.endDate
                };
                const response = await axios.post('http://127.0.0.1:7644/create_service_request', requestData);
                if (response.data.success) {
                    alert('Service request sent!');
                    this.$router.push(`/customer_home/${this.customerId}`); 
                } else {
                    console.error('Failed to submit request:', response.data.message);
                }
            } catch (error) {
                console.error('Error submitting request:', error);
            }
        }
    }
};
</script>

<style scoped>
.cust-layout {
    padding: 20px;
}
.cust-main-content {
    max-width: 600px;
    margin: auto;
}
.service-details p {
    font-size: 16px;
    margin: 5px 0;
}
.request-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.submit-btn {
    background-color: #28a745;
    color: white;
    padding: 10px;
    border: none;
    cursor: pointer;
}
.submit-btn:hover {
    background-color: #218838;
}
</style>
