<template>
  <div class="pa-4">
    <h1 class="mb-6 text-center">Capítulos do Alcorão ☪️</h1>
    <v-row>
      <v-col v-for="chapter in chapters" :key="chapter.id" cols="6" sm="6" md="4" lg="3">
        <v-btn class="h-100 w-100 pa-4" :variant="selectedChapter === chapter.id ? 'elevated' : 'flat'"
          :color="selectedChapter === chapter.id ? 'success' : 'default'" size="x-large"
          @click="selectChapter(chapter.id)">
          <div class="text-center">
            <div class="text-h5 font-weight-bold">{{ chapter.id }}</div>
            <div class="text-subtitle2">{{ chapter.name }}</div>
          </div>
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import localforage from 'localforage'
import router from '@/router'

interface Chapter {
  id: number
  name: string
}

const chapters = ref<Chapter[]>([
  { id: 1, name: 'A Abertura' },
  { id: 2, name: 'A Vaca' },
  { id: 3, name: 'A Família de Imrã' },
  { id: 4, name: 'As Mulheres' },
  { id: 5, name: 'A Mesa' },
  { id: 6, name: 'Os Rebanhos' },
  { id: 7, name: 'As Alturas' },
  { id: 8, name: 'O Saque' },
  { id: 9, name: 'O Arrependimento' },
  { id: 10, name: 'Jonas' },
])

const selectedChapter = ref<number>(1)

onMounted(async () => {
  const saved = await localforage.getItem<number>('selectedChapter')
  if (saved) {
    selectedChapter.value = saved
  }
})

const selectChapter = async (chapterId: number) => {
  selectedChapter.value = chapterId
  await localforage.setItem('selectedChapter', chapterId)

  router.push('/reading');
}
</script>
