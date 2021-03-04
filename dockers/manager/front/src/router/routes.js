
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: 'login',
        name: 'login',
        component: () => import('pages/Login.vue'),
        meta: {
          noauth: true
        }
      },
      {
        path: '',
        name: "index", component: () => import('pages/Index.vue')
      },
      {
        path: 'docker',
        name: "dockerIndex",
        redirect: '/docker/overview',
      },
      {
        path: 'docker/:tab',
        props: true,
        name: "docker",
        component: () => import("pages/Docker.vue")
      },
      {
        path: 'traefik',
        name: "traefikIndex",
        redirect: '/traefik/overview'
      },
      {
        path: 'traefik/:tab',
        props: true,
        name: "traefik",
        component: () => import("pages/Traefik.vue"),
      },
      {
        path: 'dns',
        name: "dnsIndex",
        redirect: '/dns/zones'
      },
      {
        path: 'dns/:tab',
        props: true,
        name: "dns",
        component: () => import("pages/DNS.vue")
      },
      {
        path: 'shell',
        props: true,
        name: "shellIndex",
        component: () => import("pages/Shell.vue"),
      },
      {
        path: 'shell/:tab',
        props: true,
        name: "shell",
        component: () => import("pages/Shell.vue"),
      },

    ]
  },

  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
