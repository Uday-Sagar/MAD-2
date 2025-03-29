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
    name: "CustomerSignup",
    data() {
      return {
        role: this.$route.query.role || "customer", // Default role set to "customer"
        name: "",
        email: "",
        password: "",
        confirmPassword: "",
        contact: "",
        city: "",
        locality: ""
      };
    },
    methods: {
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
            contact: this.contact,
            city: this.city,
            locality: this.locality
          });
  
          alert(response.data.message);
  
          if (response.data.success) {
            this.$router.push("/login");
          }
        } catch (error) {
          console.error("Error:", error);
          alert(error.response?.data?.message || "Something went wrong. Please try again later.");
        }
      },
  
      navigateToLogin() {
        this.$router.push("/login");
      }
    }
  };
  </script>
  