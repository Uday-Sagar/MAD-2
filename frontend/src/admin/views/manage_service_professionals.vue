<template>
  <div class="admin-layout">
    <AdminNavBar />
    <div class="admin-main-content">
      <h2>Manage Service Professionals</h2>
      <div class="search-bar">
        <input 
          type="text" 
          v-model="searchQuery" 
          class="form-control" 
          placeholder="Search by name or service type..."
        />
      </div>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Service Type</th>
            <th>Contact</th>
            <th>Flag Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="professional in filteredProfessionals" :key="professional.professional_id">
            <td>{{ professional.professional_id }}</td>
            <td>{{ professional.name }}</td>
            <td>{{ professional.email }}</td>
            <td>{{ professional.service_type }}</td>
            <td>{{ professional.contact || 'N/A' }}</td>
            <td>
              <span :class="{'text-danger': professional.is_flagged, 'text-success': !professional.is_flagged}">
                {{ professional.is_flagged ? 'Flagged' : 'Not Flagged' }}
              </span>
            </td>
            <td>
              <button
                class="btn btn-danger btn-sm me-2"
                v-if="!professional.is_flagged"
                @click="toggleFlag(professional, true)"
              >
                Flag
              </button>
              <button
                class="btn btn-success btn-sm"
                v-if="professional.is_flagged"
                @click="toggleFlag(professional, false)"
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
  name: "ManageProfessionals",
  components: { AdminNavBar },
  data() {
    return {
      professionals: [],
      searchQuery: "",
    }
  },
  mounted() {
    this.fetchProfessionals();
  },
  computed: {
    filteredProfessionals() {
      return this.professionals.filter(professional =>
        professional.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        professional.service_type.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    async fetchProfessionals() {  
      try {
        const token = localStorage.getItem("token"); // Retrieve JWT token
        const response = await axios.get('http://127.0.0.1:7644/get_service_professionals', {
          headers: { Authorization: `Bearer ${token}` } // Include JWT in headers
        });
        if (response.data.success) {
          this.professionals = response.data.professionals;
        } else {
          console.error("Failed to fetch service professionals", response.data.message);
        }
      } catch (error) {
        console.error("Error fetching professionals:", error);
      }
    },
    async toggleFlag(professional, flagStatus) {
      try {
        const token = localStorage.getItem("token"); // Retrieve JWT token
        const response = await axios.put(
          `http://127.0.0.1:7644/flag_service_professionals/${professional.professional_id}`,
          { is_flagged: flagStatus },
          {
            headers: { 
              Authorization: `Bearer ${token}`, // Include JWT in headers
              'Content-Type': 'application/json' 
            }
          }
        );
        if (response.data.success) {
          professional.is_flagged = flagStatus;  
        } else {
          console.error("Failed to update flag status:", response.data.message);
        }
      } catch (error) {
        console.error("Error updating flag status:", error);
      }
    }
  }
}
</script>

<style scoped>
.admin-main-content {
  padding: 20px;
}

.search-bar {
  margin-bottom: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  padding: 10px;
  text-align: left;
  border: 1px solid #ddd;
}

th {
  background-color: #f4f4f4;
}
</style>
