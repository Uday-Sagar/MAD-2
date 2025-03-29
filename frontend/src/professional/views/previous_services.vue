<template>
    <div class="layout">
      <ProfessionalNavBar />
      <div class="main-content">
        <h3>List of Accepted Service Requests</h3>
  
        <div v-if="loading">Loading service requests...</div>
        <div v-else-if="acceptedRequests.length === 0"><h4><strong>No active services.</strong></h4>.</div>
        <div v-else>
          <table class="service-table">
            <thead>
              <tr>
                <th>Customer Name</th>
                <th>Location</th>
                <th>Start Date</th>
                <th>End Date</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="req in acceptedRequests" :key="req.request_id">
                <td>{{ req.customer_name }}</td>
                <td>{{ req.address }}</td>
                <td>{{ req.start_date }}</td>
                <td>{{ req.end_date }}</td>
                <td>{{ req.status }}</td>
                <td>
                  <button 
                    @click="updateAction(req.request_id, 'closed')" 
                    :disabled="req.action === 'closed'">
                    {{ req.action === 'closed' ? 'Closed' : 'Close Service' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import ProfessionalNavBar from '@/professional/components/navbar.vue';
  
  export default {
    name: 'ProfessionalServices',
    components: { ProfessionalNavBar },
    data() {
      return {
        professionalId: this.$route.params.user_id,
        requests: [],
        loading: true,
      };
    },
    computed: {
      // Show both accepted and closed requests
      acceptedRequests() {
        return this.requests.filter(req => req.status === 'accepted' || req.action === 'closed');
      }
    },
    mounted() {
      this.fetchServiceRequests();
    },
    methods: {
      async fetchServiceRequests() {
        try {
          const response = await axios.get(`http://127.0.0.1:7644/get_my_requests/${this.professionalId}`);
          if (response.data.success) {
            this.requests = response.data.requests;
          } else {
            console.error('Failed to fetch requests:', response.data.message);
          }
        } catch (error) {
          console.error('Error fetching service requests:', error);
        } finally {
          this.loading = false;
        }
      },
  
      async updateAction(requestId, actionStatus) {
        try {
          const response = await axios.post(`http://127.0.0.1:7644/update_request_action`, {
            request_id: requestId,
            action: actionStatus,
          });
  
          if (response.data.success) {
            const index = this.requests.findIndex(req => req.request_id === requestId);
            if (index !== -1) {
              this.requests[index].action = actionStatus;
            }
          } else {
            console.error('Failed to update action:', response.data.message);
          }
        } catch (error) {
          console.error('Error updating action:', error);
        }
      },
    },
  };
  </script>
  