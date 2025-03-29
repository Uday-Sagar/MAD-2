<template>
  <div class="admin-layout">
    <AdminNavBar />
    <div class="admin-main-content">
      <h2>Manage Customers</h2>
      
      <table class="table table-bordered">
        <thead class="table-light">
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Contact</th>
            <th>Flag Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cust in customer" :key="cust.customer_id">
            <td>{{ cust.customer_id }}</td>
            <td>{{ cust.name }}</td>
            <td>{{ cust.email }}</td>
            <td>{{ cust.contact || 'N/A' }}</td>
            <td>
              <span :class="{'text-danger': cust.is_flagged, 'text-success': !cust.is_flagged}">
                {{ cust.is_flagged ? 'Flagged' : 'Not Flagged' }}
              </span>
            </td>
            <td>
              <button
                class="btn btn-danger btn-sm me-2"
                v-if="!cust.is_flagged"
                @click="toggleFlag(cust, true)"
              >
                Flag
              </button>
              <button
                class="btn btn-success btn-sm"
                v-if="cust.is_flagged"
                @click="toggleFlag(cust, false)"
              >
                Unflag
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import AdminNavBar from '@/admin/components/navbar.vue'
import axios from 'axios'

export default {
  name: "ManageCustomers",
  components: { AdminNavBar },
  data() {
    return {
      customer: []  
    }
  },
  mounted() {
    this.fetchCustomers();
  },
  methods: {
    async fetchCustomers() {
      try {
        const token = localStorage.getItem("token"); // Retrieve JWT token
        const response = await axios.get('http://127.0.0.1:7644/get_customers', {
          headers: { Authorization: `Bearer ${token}` } // Include JWT in headers
        });
        if (response.data.success) {
          this.customer = response.data.customers;
        } else {
          console.error("Failed to fetch customers", response.data.message);
        }
      } catch (error) {
        console.error("Error fetching customers:", error);
      }
    },
    async toggleFlag(customer, flagStatus) {
      try {
        const token = localStorage.getItem("token"); // Retrieve JWT token
        const response = await axios.put(`http://127.0.0.1:7644/flag_customer/${customer.customer_id}`,
          { is_flagged: flagStatus },
          {
            headers: { 
              Authorization: `Bearer ${token}`, // Include JWT in headers
              'Content-Type': 'application/json' 
            }
          }
        );
        if (response.data.success) {
          customer.is_flagged = flagStatus;
        } else {
          console.error("Failed to update flag status:", response.data.message);
        }
      } catch (error) {
        console.error("Error updating flag status:", error);
      }
    }
  },
};
</script>

<style scoped>
.admin-main-content {
  padding: 20px;
}

.table {
  width: 100%;
  margin-top: 20px;
}

th, td {
  padding: 10px;
  text-align: left;
}

.text-danger {
  color: red;
  font-weight: bold;
}

.text-success {
  color: green;
  font-weight: bold;
}
</style>
