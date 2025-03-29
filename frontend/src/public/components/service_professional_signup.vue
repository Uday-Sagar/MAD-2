<template>
    <div class="main-body">
      <div class="form-container">
        <h4>Sign-up to create your profile</h4>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <input v-model="name" class="form-control" type="text" placeholder="Name" required />
          </div>
          <br />
          <div class="form-group">
            <input v-model="email" class="form-control" type="email" placeholder="Mail ID" required />
          </div>
          <br />
          <div class="form-group">
            <input v-model="password" class="form-control" type="password" placeholder="Password" required />
          </div>
          <br />
          <div class="form-group">
            <input v-model="confirmPassword" class="form-control" type="password" placeholder="Confirm Password" required />
          </div>
          <br />
          <div class="mb-3">
            <label for="service_type" class="form-label">Service Type:</label>
            <select id="service_type" v-model="service_type" class="form-control" required>
              <option value="" disabled>Select a service</option>
              <option v-for="service in services" :key="service.id" :value="service.id">
                {{ service.name }}
              </option>
            </select>
          </div>
          <br />
          <div class="form-group">
            <input v-model="experience" class="form-control" type="text" placeholder="Experience (in years)" required/>
          </div>
          <br />
          <div class="form-group">
            <input v-model="contact" class="form-control" type="text" placeholder="Contact" required/>
          </div>
          <br />
          <div class="form-group">
            <input v-model="city" class="form-control" type="text" placeholder="City" required/>
          </div>
          <br />
          <div class="form-group">
            <input v-model="locality" class="form-control" type="text" placeholder="Locality" required/>
          </div>
          <br />
          <div class="form-group">
            <textarea v-model="description" class="form-control" placeholder="Short description about your service"></textarea>
          </div>
          <br />
          <button type="submit" class="btn btn-success">Sign Up</button>
          <p style="margin-top: 1rem">
            Already Registered?
            <button class="btn btn-primary" @click="navigateToLogin">Login</button>
          </p>
        </form>
      </div>
    </div>
</template>
  
<script>
import axios from "axios";

export default {
name: "ServiceProfessionalSignup",
data() {
    return {
    role: this.$route.query.role || "service_professional",
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    service_type: "",
    experience: "",
    contact: "",
    city: "",
    locality: "",
    description: "",
    services: [] // Stores the list of available services
    };
},
methods: {
    async fetchServices() {
    try {
        const response = await axios.get("http://127.0.0.1:7644/get_professional_services");
        if (response.data.success) {
        this.services = response.data.services;
        } else {
        console.error("Failed to fetch services:", response.data.message);
        }
    } catch (error) {
        console.error("Error fetching services:", error);
    }
    },

    async handleSubmit() {
    if (this.password !== this.confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    try {
        const response = await axios.post("http://127.0.0.1:7644/signup", {
        role: this.role,
        name: this.name,
        email: this.email,
        password: this.password,
        service_type: this.service_type, 
        experience: this.experience,
        contact: this.contact,
        city: this.city,
        locality: this.locality,
        description: this.description
        });

        alert(response.data.message);
        if (response.data.success) {
        this.$router.push("/login");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong. Please try again later.");
    }
    },

    navigateToLogin() {
    this.$router.push("/login");
    }
},
mounted() {
    this.fetchServices(); // Fetch services when the component loads
}
};
</script>
  