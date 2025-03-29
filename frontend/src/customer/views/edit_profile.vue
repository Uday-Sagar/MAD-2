<template>
    <div class="layout">
        <CustomerNavBar />
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
                    <label for="contact" class="form-label">Contact:</label>
                    <input type="text" id="contact" v-model="profile.contact" class="form-control" />
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
                <button type="submit" class="btn btn-primary" style="width:15%">Save Changes</button>
            </form>
            <br>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import CustomerNavBar from '@/customer/components/navbar.vue';

export default {
    name: 'EditCustomerProfile',
    components: { CustomerNavBar },

    data() {
        return {
            profile: {
                name: '',
                email: '',
                contact: '',
                city:'',
                locality:'',
            },
        };
    },
    methods: {
        async fetchProfile() {
            try {
                const userId = this.$route.params.user_id;
                const response = await axios.get(`http://127.0.0.1:7644/get_customer_profile/${userId}`);

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
                const userId = this.$route.params.user_id;
                const response = await axios.put(
                    `http://127.0.0.1:7644/update_customer_profile/${userId}`,
                    this.profile);

                if (response.data.success) {
                    alert('Profile updated successfully');
                    this.$router.push(`/customer_profile/${userId}`);
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
    }
};
</script>
