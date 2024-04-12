// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  typescript: {
    typeCheck: true
  },
  modules: [
    'nuxt-primevue',
    '@sidebase/nuxt-auth'
  ],
  primevue: {
    components: {
      include: ['Button']
    }
  },
  css: [
    'primeicons/primeicons.css', //css dos ícones do primevue
    'primevue/resources/themes/aura-light-green/theme.css', // css tema dos componentes primevue
    '~/assets/style/global-variables.scss',  //variáveis css global customizado para toda a aplicação
    '~/assets/style/global-project.scss',  //css global customizado para toda a aplicação
  ],
  auth: {
    baseURL: process.env.BACKEND_URL, // Endereço do Backend
    provider: {
      type: 'local', // Web Token
      endpoints: {
        signIn: { path: '/token/login', method: 'post' }, //rota do login
        signOut: { path: '/token/logout', method: 'post' }, //rota do logout
        signUp: { path: '', method: 'get' }, //rota de cadastro
        getSession: { path: '/users', method: 'get' }, //rota autenticada para verificação se foi autenticado c/ sucesso
        //refresh: { } //rota para renovar o token (somente no type refresh)
      },
      token: {
        signInResponseTokenPointer: '/auth_token', //indica o local do token access na resposta do backend
        //maxAgeInSeconds: 600 //validade do token access
        type: 'Token'
      },
      // refreshToken: { 
      //   signInResponseRefreshTokenPointer: '', //local do token refresh
      //   maxAgeInSeconds: 600, //validade do token refresh
      // },
      pages: {
        login: '/' //endereço (rota) da página de login
      }
    }
  }
})
