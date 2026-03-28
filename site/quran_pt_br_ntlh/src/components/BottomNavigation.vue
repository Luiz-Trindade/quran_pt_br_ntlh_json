<template>
    <v-bottom-navigation grow :model-value="currentRoute" bg-color="green-darken-4">
        <v-btn value="chapters" @click="navigate('')">
            <v-icon>mdi-book-open</v-icon>
            <span>Capítulos</span>
        </v-btn>

        <v-btn value="reading" @click="navigate('reading')">
            <v-icon>mdi-book-open-page-variant</v-icon>
            <span>Leitura</span>
        </v-btn>

        <v-btn value="settings" @click="navigate('settings')">
            <v-icon>mdi-cog</v-icon>
            <span>Configurações</span>
        </v-btn>
    </v-bottom-navigation>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { computed } from 'vue'

const router = useRouter()
const route = useRoute()

const currentRoute = computed(() => {
    if (route.path === '/') return 'chapters'
    return route.path.slice(1) || 'chapters'
})

const navigate = (routeName: string) => {
    router.push(`/${routeName}`)
}
</script>