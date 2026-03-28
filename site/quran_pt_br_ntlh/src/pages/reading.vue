<template>
    <div class="pa-md-4 pa-2">
        <h1 class="mb-2 text-center text-h4 text-md-h3 font-weight-bold">Leitura do Alcorão</h1>
        <p class="text-center text-subtitle2 text-md-subtitle1 mb-8 text-grey-darken-1">
            Explore os versículos sagrados
        </p>

        <!-- Cabeçalho da Sura -->
        <div v-if="currentSura" class="text-center mb-6">
            <h2 class="text-h5 font-weight-bold">
                {{ currentSura.id }}. {{ currentSura.transliteration }}
            </h2>
            <p class="text-h6 text-grey-darken-2">{{ currentSura.name }}</p>
            <p class="text-body2 text-grey-darken-1">{{ currentSura.translation }}</p>
        </div>

        <div v-if="ayats.length" class="mt-6">
            <v-card v-for="ayat in ayats" :key="ayat.id" class="mb-4" elevation="2" hover>
                <v-card-text class="py-6 px-4 px-md-6">
                    <div class="d-flex flex-column flex-md-row gap-4 align-md-center">
                        <v-row>
                            <v-col>
                                <div class="flex-grow-1 min-w-0">
                                    <div class="d-flex align-start gap-3 mb-3">
                                        <v-chip color="success" text-color="white" size="small"
                                            class="font-weight-bold flex-shrink-0">
                                            {{ ayat.number }}
                                        </v-chip>
                                    </div>
                                    <p class="text-body1 text-md-h6 mb-0 text-justify text-white"
                                        style="line-height: 1.85; letter-spacing: 0.4px;">
                                        {{ ayat.translation_pt }}
                                    </p>
                                </div>

                                <v-divider class="ma-5" />

                                <!-- Botões -->
                                <div class="d-flex justify-center gap-4">
                                    <v-btn icon="mdi-content-copy" size="large" variant="text" color="success"
                                        @click="copyToClipboard(ayat.translation_pt, ayat)" title="Copiar versículo">
                                    </v-btn>

                                    <v-btn icon="mdi-volume-high" size="large" variant="text" color="success"
                                        @click="speakAyat(ayat.translation_pt)" :disabled="isSpeaking"
                                        title="Ler em voz alta">
                                    </v-btn>
                                </div>
                            </v-col>
                        </v-row>
                    </div>
                </v-card-text>
            </v-card>
        </div>

        <v-empty-state v-else-if="!loading" icon="mdi-book-open-page-variant" headline="Nenhum versículo carregado"
            text="Selecione um capítulo para começar a leitura" />

        <div v-if="loading" class="text-center py-12">
            <v-progress-circular indeterminate color="success" size="60" />
            <p class="mt-4 text-grey-darken-1">Carregando sura...</p>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import localforage from 'localforage';

interface Verse {
    id: number;
    number: number;
    text: string;
    translation?: string;
    translation_pt: string;
}

interface Sura {
    id: number;
    name: string;
    transliteration: string;
    translation: string;
    type?: string;
    total_verses: number;
    verses: Verse[];
}

const route = useRoute();
const ayats = ref<Verse[]>([]);
const currentSura = ref<Sura | null>(null);
const loading = ref(false);
const isSpeaking = ref(false);

const loadSura = async (suraId: string | string[]) => {
    const id = Number(suraId);
    if (!id || isNaN(id)) return;

    loading.value = true;
    ayats.value = [];
    currentSura.value = null;

    try {
        // Carrega apenas o arquivo da sura selecionada
        const paddedId = id.toString().padStart(3, '0');
        const response = await fetch(`/suras/sura-${paddedId}.json`);

        if (!response.ok) {
            throw new Error(`Sura ${id} não encontrada`);
        }

        const suraData: Sura = await response.json();

        currentSura.value = suraData;
        ayats.value = suraData.verses.map(v => ({
            id: v.id,
            number: v.number || v.id,
            text: v.text,
            translation_pt: v.translation_pt
        }));

        // Salva o capítulo selecionado para uso no copy
        await localforage.setItem('selectedChapter', id);

    } catch (error) {
        console.error('Erro ao carregar sura:', error);
        ayats.value = [];
    } finally {
        loading.value = false;
    }
};

// Observa mudanças na rota (ex: /reading/5 ou /sura/42)
watch(() => route.params.id, (newId) => {
    if (newId) loadSura(newId);
}, { immediate: true });

// Fallback: se não vier pela rota, tenta pegar do localforage
onMounted(async () => {
    const savedChapter = await localforage.getItem('selectedChapter');
    if (savedChapter && !route.params.id) {
        loadSura(savedChapter as string);
    }
});

// ==================== Funções de Ação ====================
const speakAyat = (text: string) => {
    if (!('speechSynthesis' in window)) {
        alert('Seu navegador não suporta leitura em voz alta.');
        return;
    }

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'pt-BR';
    utterance.rate = 0.95;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    utterance.onend = () => isSpeaking.value = false;
    utterance.onerror = () => {
        isSpeaking.value = false;
        alert('Não foi possível reproduzir o áudio.');
    };

    isSpeaking.value = true;
    window.speechSynthesis.speak(utterance);
};

const copyToClipboard = async (text: string, ayat: Verse) => {
    const selectedChapter = Number((await localforage.getItem('selectedChapter')) || 1);
    const formattedText = `"${text}"\n\n(Alcorão, Capítulo ${selectedChapter}, Versículo ${ayat.number})`;

    navigator.clipboard.writeText(formattedText).then(() => {
        alert('Versículo copiado!');
    }).catch(() => alert('Erro ao copiar.'));
};
</script>