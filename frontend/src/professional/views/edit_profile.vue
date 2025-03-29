<template>
    <div class="layout">
        <ProfessionalNavBar />
        <div class="main-content">
            <h1>Edit Profile</h1>
            <form @submit.prevent="updateProfile">
                <div class="mb-3">
                    <label for="name" class="form-label">Name:</label>
                    <input type="text" id="name" v-model="profile.name" class="form-control" />
                </div>
                <br>
                <div class="mb-3">
                    <label for="email" class="form-label">Email:</label>
                    <input type="email" id="email" v-model="profile.email" class="form-control" />
                </div>
                <br>
                <div class="mb-3">
                    <label for="service_type" class="form-label">Service Type:</label>
                    <select id="service_type" v-model="profile.service_type" class="form-control">
                        <option v-for="service in services" :key="service.id" :value="service.name">
                            {{ service.name }}
                        </option>
                    </select>
                </div>
                <br>
                <div class="mb-3">
                    <label for="experience" class="form-label">Experience (Years):</label>
                    <input type="number" id="experience" v-model="profile.experience" class="form-control" />
                </div>
                <br>
                <div class="mb-3">
                    <label for="city" class="form-label">City:</label>
                    <input type="text" id="city" v-model="profile.city" class="form-control" />
                </div>
                <br>
                <div class="mb-3">
                    <label for="locality" class="form-label">Locality:</label>
                    <input type="text" id="locality" v-model="profile.locality" class="form-control" />
                </div>
                <br>
                <div class="mb-3">
                    <label for="contact" class="form-label">Contact:</label>
                    <input type="text" id="contact" v-model="profile.contact" class="form-control" />
                </div>
                <br>
                <div class="mb-3">
                    <label for="description" class="form-label">Description:</label>
                    <textarea id="description" v-model="profile.description" rows="4" class="form-control"></textarea>
                </div>
                <br>
                <button type="submit" class="btn btn-primary" style="width:15%">Save Changes</button>
            </form>
            <br>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import ProfessionalNavBar from '@/professional/components/navbar.vue';

export default {
    name: 'EditProfessionalProfile',
    components: { ProfessionalNavBar },

    data() {
        return {
            profile: {
                name: '',
                email: '',
                service_type: '',
                experience: '',
                contact: '',
                city:'',
                locality:'',
                description: ''
            },
            services: [] // Store available services
        };
    },
    methods: {
        async fetchServices() {
            try {
                const response = await axios.get('http://127.0.0.1:7644/get_professional_services');
                if (response.data.success) {
                    this.services = response.data.services;
                } else {
                    console.error("Failed to fetch services:", response.data.message);
                }
            } catch (error) {
                console.error("Error fetching services:", error);
            }
        },
        async fetchProfile() {
            try {
                const token = localStorage.getItem('access_token');
                const userId = this.$route.params.user_id;
                const response = await axios.get(`http://127.0.0.1:7644/get_professional_profile/${userId}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });

                if (response.data.success) {
                    this.profile = response.data.data;
                } else {
                    console.error("Failed to load profile.", response.data.message);
                }
            } catch (error) {
                console.error("Error fetching profile:", error);
            }
        },
        async updateProfile() {
            try {
                const token = localStorage.getItem('access_token');
                const userId = this.$route.params.user_id;
                const response = await axios.put(
                    `http://127.0.0.1:7644/update_professional_profile/${userId}`,
                    this.profile,
                    { headers: { Authorization: `Bearer ${token}` } }
                );

                if (response.data.success) {
                    alert('Profile updated successfully');
                    this.$router.push(`/professional_profile/${userId}`);
                } else {
                    console.error("Failed to update profile.", response.data.message);
                }
            } catch (error) {
                console.error("Error updating profile:", error);
            }
        }
    },
    mounted() {
        this.fetchProfile();
        this.fetchServices();
    }
};
</script>
