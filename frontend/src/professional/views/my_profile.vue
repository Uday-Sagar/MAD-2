<template>
    <div class="layout">
        <ProfessionalNavBar />
        <div class="main-content">            
            <div v-if="loading">Loading profile...</div>
            <div v-else-if="errorMessage" class="error">{{ errorMessage }}</div>
            <div v-else-if="professional" class="profile-card">
                <div class="profile-header">
                    <h2>{{ professional.name }}</h2>
                </div>
                <div class="profile-details">
                    <p><strong>Email:</strong> {{ professional.email }}</p>
                    <p><strong>Experience:</strong> {{ professional.experience }} years</p>
                    <p><strong>Service Type:</strong> {{ professional.service_type }} </p>
                    <p><strong>Contact:</strong> {{ professional.contact }}</p>
                    <p><strong>City:</strong> {{ professional.city }}</p>
                    <p><strong>Locality:</strong> {{ professional.locality }}</p>
                    <p><strong>Description:</strong> {{ professional.description }}</p>
                </div>
                <div class="edit-button-container">
                    <button class="edit-button" @click="editProfile">Edit Profile</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import ProfessionalNavBar from '@/professional/components/navbar.vue';

export default {
    name: 'ProfessionalProfile',
    components: { ProfessionalNavBar },
    data() {
        return {
            professional: null,
            loading: true,
            errorMessage: ''
        };
    },
    async created() {
        try {
            const userId = this.$route.params.user_id;  
            
            if (!userId) {
                this.errorMessage = "User ID is missing in the route.";
                this.loading = false;
                return;
            }
            const response = await axios.get(`http://127.0.0.1:7644/get_professional_profile/${userId}`);

            if (response.data.success) {
                this.professional = response.data.data;
            } else {
                this.errorMessage = response.data.message || "Failed to fetch profile.";
            }
        } catch (error) {
            console.error("Error fetching profile:", error);
            this.errorMessage = "Error loading profile. Please try again.";
        } finally {
            this.loading = false;
        }
    },
    methods: {
        editProfile() {
            const userId = this.$route.params.user_id; 
            this.$router.push(`/edit_professional_profile/${userId}`);
        }
    }
};
</script>