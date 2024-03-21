<script setup lang="ts">
    definePageMeta({
        middleware: 'auth' // Essa tela será privada
    })
</script>

<template>
    <div>
        <h1>Olá Tela Home!</h1>
    </div>
</template>