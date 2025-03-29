<template>
    <div class="cust-layout">
      <CustomerNavBar />
      <div class="cust-main-content">
        <h3>Modify your service request details below:</h3>
        <div class="update-request-container">
  
          <div v-if="loading" class="loading">Loading request details...</div>
          <div v-else>
            <form @submit.prevent="submitUpdate">
              <div class="form-group">
                <label>Service Type:</label>
                <input type="text" v-model="request_details.service_type" disabled />
              </div>
  
              <div class="form-group">
                <label>Professional:</label>
                <input type="text" v-model="request_details.professional_name" disabled />
              </div>
  
              <div class="form-group">
                <label>Location:</label>
                <input type="text" v-model="request_details.location" />
              </div>
  
              <div class="form-group">
                <label>Start Date:</label>
                <input type="date" v-model="request_details.start_date" />
              </div>
  
              <div class="form-group">
                <label>End Date:</label>
                <input type="date" v-model="request_details.end_date" />
              </div>

              <button type="submit" class="submit-btn">Update Request</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import CustomerNavBar from '@/customer/components/navbar.vue';
  
  export default {
    name: 'UpdateServiceRequest',
    components: { CustomerNavBar },
    data() {
      return {
        userId: this.$route.params.user_id,
        requestId: this.$route.params.request_id,
        request_details: {
            service_type: '',
            professional_name: '',
            location: '',
            start_date: '',
            end_date: '',
        },
        loading: true,
      };
    },
    mounted() {
      this.fetchRequestDetails();
    },
    methods: {
      async fetchRequestDetails() {
        try {
          const response = await axios.get( `http://127.0.0.1:7644/get_service_request/${this.requestId}`);
          if (response.data.success) {
            this.request_details = response.data.service_request;
          } else {
            console.error('Failed to fetch service request:', response.data.message);
          }
        } catch (error) {
          console.error('Error fetching service request:', error);
        } finally {
          this.loading = false;
        }
      },
  
      async submitUpdate() {
        try {
          const response = await axios.put(`http://127.0.0.1:7644/update_service_request/${this.requestId}`, {
            requestId: this.requestId,
            userId: this.userId,
            ...this.request_details,
          });
          if (response.data.success) {
            alert('Service request updated successfully!');
            this.$router.push(`/customer_service_requests/${this.userId}`);
          } else {
            alert('Failed to update service request: ' + response.data.message);
          }
        } catch (error) {
          console.error('Error updating service request:', error);
          alert('An error occurred while updating the request.');
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .update-request-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
  }
  
  h1, h3 {
    text-align: center;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    font-weight: bold;
  }
  
  input, select {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .submit-btn {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .submit-btn:hover {
    background-color: #0056b3;
  }
  
  .loading {
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    color: #666;
  }
  </style>
  