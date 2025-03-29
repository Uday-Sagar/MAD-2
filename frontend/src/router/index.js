import { createRouter, createWebHistory } from 'vue-router';

import LoginPage from '@/public/components/login_page.vue';
import SignupPage from '@/public/components/signup_page.vue';
import CustomerSignup from '@/public/components/customer_singup.vue';
import ServiceProfessionalSignup from '@/public/components/service_professional_signup.vue';
import LandingPage from '@/public/views/landing_page.vue';

import AdminHome from '@/admin/views/admin_home.vue';
import ProfessionalRequest from '@/admin/views/professional_request.vue';
import ManageCustomers from '@/admin/views/manage_customers.vue';
import ManageProfessionals from '@/admin/views/manage_service_professionals.vue';
import ManageServices from '@/admin/views/manage_services.vue';
import AddService from '@/admin/views/add_service.vue';
import EditService from '@/admin/views/edit_service.vue';

import CustomerHome from '@/customer/views/customer_home.vue';
import CreateServiceRequest from '@/customer/views/create_service_request.vue';
import SelectServiceProfessional from '@/customer/views/select_service_professional.vue';
import CustomerServiceRequests from '@/customer/views/my_service_requests.vue';
import CustomerProfile from  '@/customer/views/my_profile.vue';
import EditCustomerProfile from '@/customer/views/edit_profile.vue';
import UpdateServiceRequest from '@/customer/views/update_service_request.vue';
import CustomerServiceRatings from '@/customer/views/review_services.vue';
import SubmitRatings from '@/customer/views/submit_rating.vue';

import ProfessionalHome from '@/professional/views/home.vue';
import ProfessionalProfile from '@/professional/views/my_profile.vue';
import ProfessionalServices from '@/professional/views/previous_services.vue';
import EditProfessionalProfile from '@/professional/views/edit_profile.vue';

const routes=[
    {
        path:"/",
        component: LandingPage,
    },      
    {
        path:"/login",
        component: LoginPage
    },
    {
        path:"/signup",
        component: SignupPage,
    },
    {
        path:"/customer_signup",
        component: CustomerSignup,
        props: route => ({ role: route.query.role }),
    },
    {
        path:"/service_professional_signup",
        component:ServiceProfessionalSignup, 
        props: route => ({ role: route.query.role }), 
    },
    // ------------------- Admin paths -------------------

    {
        path:"/admin_home",
        component: AdminHome,
    },
    {
        path: "/service_professional_request",
        component: ProfessionalRequest,
    },
    {
        path: "/manage_customers",
        component: ManageCustomers,
    },
    {
        path: "/manage_service_professionals",
        component: ManageProfessionals,
    },
    {
        path: "/manage_services",
        component: ManageServices,
    },
    {
        path: "/add_services",
        component: AddService,
    },
    {
        path: "/edit_service/:id",
        component: EditService,
    },

    // ------------------- Customer paths -------------------

    {
        path:"/customer_home/:user_id",
        component: CustomerHome,
    },
    {
        path: "/select_service_professional",
        component: SelectServiceProfessional,
        props: route => ({
            serviceType: route.query.serviceType,
            userId: route.query.user_id
        })
    },
    {
        path: "/create_service_request",
        component: CreateServiceRequest,
        props: route => ({
            serviceType: route.query.serviceType,
            professionalId: route.query.professionalId,
            userId: route.query.user_id,
        })
    },
    {
        path: "/update_service_request/:user_id/:request_id",
        component: UpdateServiceRequest
    },
    {
        path: "/customer_profile/:user_id",
        component: CustomerProfile,
    },
    {
        path: "/customer_service_requests/:user_id",
        component: CustomerServiceRequests,
    },
    {
        path: "/edit_customer_profile/:user_id",
        component: EditCustomerProfile,
    },
    {
        path: "/rate_services/:user_id",
        component: CustomerServiceRatings,
    },
    {
        path: '/submit_rating/:user_id/:service_id',
        component: SubmitRatings
    },

    // ------------------- Service Professional paths -------------------

    {
        path:"/professional_home/:user_id",
        component: ProfessionalHome,
    },
    {
        path:"/professional_profile/:user_id",
        component: ProfessionalProfile,
    },
    {
        path:"/previous_services/:user_id",
        component: ProfessionalServices,
    },
    {
        path:"/edit_professional_profile/:user_id",
        component: EditProfessionalProfile,

    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
  });
  
  export default router;