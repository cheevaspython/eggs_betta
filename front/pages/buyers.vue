<template>
  <div class="buyers">
    <ul class="buyers-list">
      <li class="buyers-list__add" @click="createNewBuyer">Добавить покупателя</li>
      <li v-for="buyer in buyers" @click="onBuyersClick(buyer)" :key="buyer.name" class="buyers-list__item">
        {{ buyer.name }} / {{ buyer.inn }}
      </li>
    </ul>
    <transition name="fade">
      <BuyerCard :trader-data="activeBuyer" v-show="showBuyer"/>
    </transition>
  </div>
</template>

<script>
import ModalCreateBuyerForm from '@/components/forms/ModalCreateBuyerForm'
export default {
  name: "buyers",
  components: {
    BuyerCard: () => import("@/components/cards/BuyerCard"),
  },
  data() {
    return {
      activeBuyer: {},
      showBuyer: false,
    }
  },
  // middleware: 'auth',
  async created() {
    await this.$store.dispatch('ca/getBuyers')
  },
  methods: {
    async createNewBuyer() {
      const acceptedRoles = ['6', '8']
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
        component: ModalCreateBuyerForm,
        hasModalCard: true,
        trapFocus: true
      })
    },
    onBuyersClick(buyer) {
      if (this.activeBuyer == buyer) {
        this.showBuyer = !this.showBuyer
      }
      else {
        this.activeBuyer = buyer, 
        this.showBuyer = true
      }
    }
  },
  computed: {
    buyers() {
      return this.$store.state.ca.buyers
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

.buyers {
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

.buyers-list {
  &__add {
    cursor: pointer;
    text-align: center;
    padding: 5px;
    background-color: #f8f8f8;
    border-radius: 10px;
    border-bottom: 1px solid #f2f2f2;

    &:hover {
      background-color: #41e33858;
    }
  }

  &__item {
    cursor: pointer;
    padding: 5px;
    background-color: #f8f8f8;
    border-radius: 10px;
    border-bottom: 1px solid #f2f2f2;

    &:hover {
      color: #1e6ac8e8;
      background-color: #f2f2f2;
    }
  }
}
</style>
