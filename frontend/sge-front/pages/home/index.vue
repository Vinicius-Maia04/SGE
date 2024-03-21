<script setup lang="ts">

    const { signOut } = useAuth();

    const submitSignOut =  () => {        
        signOut({ redirect: false })
        .then(()=>{
            console.log('Successfully logged out!');
            navigateTo('/');
        })
         .catch((error)=>{
            console.log('Error trying to logout: ', error);
        });
    }

    definePageMeta({
        middleware: 'auth' // Essa tela será privada
    })
</script>

<template>
    <div>
        <h1>Olá Tela Home!</h1>
        <button @click="submitSignOut" class="customButton">SAIR</button>
    </div>
</template>