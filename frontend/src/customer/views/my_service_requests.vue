<template>
  <div class="cust-layout">
    <CustomerNavBar />
    <div class="cust-main-content">
      <h1>My Service Requests</h1>
      <h3>Below is the list of all your service requests and their status.</h3>

      <div v-if="loading" class="loading">Loading service requests...</div>
      <div v-else-if="serviceRequests.length === 0" class="no-requests">
        No service requests found.
      </div>
      <div v-else class="service-requests">
        <table class="styled-table">
          <thead>
            <tr>
              <th>Request ID</th>
              <th>Service Type</th>
              <th>Professional</th>
              <th>Location</th>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Status</th>
              <th>Action</th>
              <th>Update</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service_request in serviceRequests" :key="service_request.id">
              <td>{{ service_request.id }}</td>
              <td>{{ service_request.serviceType }}</td>
              <td>{{ service_request.professionalName }}</td>
              <td>{{ service_request.location }}</td>
              <td>{{ service_request.startDate }}</td>
              <td>{{ service_request.endDate || 'N/A' }}</td>
              <td>{{ service_request.status }}</td>
              <td>
                <button 
                  v-if="(service_request.status === 'accepted' || service_request.status === 'rejected') && service_request.action !== 'closed'" 
                  @click="closeService(service_request.id)" 
                  class="close-btn">
                  Close Service
                </button>
                <span v-else-if="service_request.action === 'closed'">Closed</span>
              </td>
              <td>
                <button 
                  v-if="(service_request.status === 'pending' || service_request.status === 'accepted') && service_request.action === 'open'" 
                  @click="updateRequest(service_request)" 
                  class="update-btn">
                  Update Request
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
import CustomerNavBar from '@/customer/components/navbar.vue';

export default {
  name: 'CustomerServiceRequests',
  components: { CustomerNavBar },
  data() {
    return {
      userId: this.$route.params.user_id, 
      serviceRequests: [],
      loading: true,
    };
  },
  mounted() {
    this.fetchServiceRequests();
  },
  methods: {
    async fetchServiceRequests() {
      try {
        const response = await axios.get(`http://127.0.0.1:7644/get_service_requests_by_user/${this.userId}`);

        if (response.data.success) {
          this.serviceRequests = response.data.serviceRequests;
        } else {
          console.error('Failed to fetch service requests:', response.data.message);
        }
      } catch (error) {
        console.error('Error fetching service requests:', error);
      } finally {
        this.loading = false;
      }
    },
    updateRequest(service_request) {
      this.$router.push({
        path: `/update_service_request/${this.userId}/${service_request.id}`,
      });
    },
    async closeService(requestId) {
      try {
        const response = await axios.post(`http://127.0.0.1:7644/update_request_action`, {
          request_id: requestId,
          action: 'closed',
        });

        if (response.data.success) {
          // Update UI to reflect closed service
          const index = this.serviceRequests.findIndex(req => req.id === requestId);
          if (index !== -1) {
            this.serviceRequests[index].action = 'closed';
          }
        } else {
          console.error('Failed to close service:', response.data.message);
        }
      } catch (error) {
        console.error('Error closing service:', error);
      }
    }
  }
};
</script>

<style scoped>
/* Table Container */
.service-requests {
  margin-top: 20px;
  overflow-x: auto;
}

/* Table Styling */
.styled-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  overflow: hidden;
}

/* Table Header */
.styled-table thead {
  background-color: #007bff;
  color: white;
  text-align: left;
  font-weight: bold;
}

.styled-table th {
  padding: 12px;
  text-transform: uppercase;
}

/* Table Rows */
.styled-table td {
  padding: 12px;
  border-bottom: 1px solid #ddd;
}

/* Alternate Row Colors */
.styled-table tbody tr:nth-child(odd) {
  background-color: #f9f9f9;
}

/* Buttons */
.update-btn, .close-btn {
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.update-btn {
  background-color: #28a745;
}

.update-btn:hover {
  background-color: #218838;
}

.close-btn {
  background-color: #dc3545;
}

.close-btn:hover {
  background-color: #c82333;
}
</style>
