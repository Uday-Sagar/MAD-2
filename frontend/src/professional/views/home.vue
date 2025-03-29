<template>
  <div class="layout">
    <ProfessionalNavBar />
    <div class="main-content">
      <h3>List of Assigned Service Requests</h3>

      <div v-if="loading">Loading service requests...</div>
      <div v-else-if="pendingRequests.length === 0"><h4><strong>No pending service requests found.</strong></h4></div>
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
            <tr v-for="req in pendingRequests" :key="req.request_id">
              <td>{{ req.customer_name }}</td>
              <td>{{ req.address }}</td>
              <td>{{ req.start_date }}</td>
              <td>{{ req.end_date }}</td>
              <td>{{ req.status }}</td>
              <td>
                <button @click="updateRequestStatus(req.request_id, 'accepted')">Accept</button>
                <button @click="updateRequestStatus(req.request_id, 'rejected')">Reject</button>
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
  name: 'ProfessionalHome',
  components: { ProfessionalNavBar },
  data() {
    return {
      professionalId: this.$route.params.user_id,
      requests: [],
      loading: true,
    };
  },
  computed: {
    // This will only contain requests that are pending
    pendingRequests() {
      return this.requests.filter(req => req.status === 'pending' && req.action === 'open');
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

    async updateRequestStatus(requestId, status) {
      try {
        const response = await axios.post(`http://127.0.0.1:7644/update_request_status`, {
          request_id: requestId,
          status,
        });

        if (response.data.success) {
          this.requests = this.requests.filter(req => req.request_id !== requestId);
        } else {
          console.error('Failed to update status:', response.data.message);
        }
      } catch (error) {
        console.error('Error updating request status:', error);
      }
    },
  },
};
</script>

