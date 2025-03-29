<template>
    <AdminNavBar />
    <div class="admin-main-content">
      <h1>This is the Admin home page</h1>
      <h3>This page shows statistics of the website.</h3>
    </div>

</template>

<script>
import axios from 'axios';
import AdminNavBar from '@/admin/components/navbar.vue';

export default {
  name: "AdminHome",
  components: { AdminNavBar },
};
</script>
