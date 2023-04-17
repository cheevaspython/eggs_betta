<template>
  <div class="logists">
    <ul class="logists-list">
      <li class="logists-list__add" @click="createNewLogic">Добавить логиста</li>
      <li v-for="logic in logists" @click="onLogicClick(logic)" :key="logic.id" class="logists-list__item">
        {{ logic.name }} / {{ logic.inn }}
      </li>
    </ul>
    <transition name="fade">
      <LogicCard :trader-data="activeLogic" v-show="showLogic"/>
    </transition>
  </div>
</template>

<script>
import LogicCard from "@/components/cards/LogicCard";
import ModalCreateLogicForm from '@/components/forms/ModalCreateLogicForm'
export default {
  name: "logistic",
  components: {
    LogicCard,
  },
  data() {
    return {
      activeLogic: null,
      showLogic: false,
    }
  },
  methods: {
    async createNewLogic() {
      const acceptedRoles = ['4', '6', '8']
      const userRole = localStorage.getItem('userRole')
      if (!acceptedRoles.includes(userRole)) {
        return alert('Доступ запрещен')
      }
      const password = prompt('Введите пароль')
      if (password == '') {
        return alert('Доступ запрещен')
      }
      const checkPassword = await this.$store.dispatch('user/masterPassword', password)
      if (!checkPassword) {
        return alert('Доступ запрещен')
      }
      this.$buefy.modal.open({
        parent: this,
        component: ModalCreateLogicForm,
        hasModalCard: true,
        trapFocus: true
      })
    },
    onLogicClick(logic) {
      if (this.activeLogic == logic) {
        this.showLogic = !this.showLogic
      }
      else {
        this.activeLogic = logic, 
        this.showLogic = true
      }
    }
  },
  async created() {
    await this.$store.dispatch('ca/getLogists')
  },
  computed: {
    logists() {
      return this.$store.state.ca.logists
    }
  }
}
</script>

<style lang="scss" scoped>
ul {
  list-style-type: none;
  max-height: 85vh;
  overflow-y: scroll;
}

.logists {
  display: grid;
  grid-template-columns: 1fr 1fr;
  margin-left: 0;
}

.fade-enter-active {
  transition: all .4s ease;
}
.fade-leave-active {
  transition: all .4s ease;
}
.fade-enter, .fade-leave-to {
  transform: translateX(50px);
  opacity: 0;
}

.logists-list {
  &__add {
    cursor: pointer;
    text-align: center;
    padding: 5px;
    background-color: #f8f8f8;
    border-bottom: 1px solid #f2f2f2;
    border-radius: 10px;

    &:hover {
      background-color: #41e33858;
    }
  }

  &__item {
    cursor: pointer;
    padding: 5px;
    background-color: #f8f8f8;
    border-bottom: 1px solid #f2f2f2;
    border-radius: 10px;

    &:hover {
      color: #1e6ac8e8;
      background-color: #f2f2f2;
    }
  }

}
</style>
