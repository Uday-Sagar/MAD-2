<template>
  <div class="main-body">
    <div class="form-container">
      <h4>Select Your Role</h4>
      <form @submit.prevent="handleRoleSelection">
        <div class="form-group">
          <select class="form-control" v-model="role" required>
            <option value="" disabled selected>Choose a role</option>
            <option value="customer">Customer</option>
            <option value="service_professional">Service professional</option>
          </select>
        </div>
        <br>
        <button type="submit" class="btn btn-success">Continue</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "RoleSelectionPage",
  data() {
    return {
      role: ""
    };
  },
  methods: {
    handleRoleSelection() {
      if (this.role) {
        this.$router.push({ path: `/${this.role}_signup`, query: { role: this.role } });
      }
    }
  }
};
</script>
