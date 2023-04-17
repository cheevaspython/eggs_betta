<template>
  <div class="sellers">
    <ul class="sellers-list">
      <li class="sellers-list__add" @click="createNewSeller">Добавить продавца</li>
      <li v-for="seller in sellers" @click="onSellerClick(seller)" :key="seller.id" class="sellers-list__item">
        {{ seller.name }} / {{ seller.inn }}
      </li>
    </ul>
    <transition name="fade">
      <SellerCard :trader-data="activeSeller" v-show="showSeller"/>
    </transition>
  </div>
</template>

<script>
import ModalCreateSellerForm from '@/components/forms/ModalCreateSellerForm'
export default {
  name: "sellers",
  components: {
    SellerCard: () => import("@/components/cards/SellerCard"),
  },
  data() {
    return {
      activeSeller: {},
      showSeller: false
    }
  },
  methods: {
    onSellerClick(seller) {
      if (this.activeSeller == seller) {
        this.showSeller = !this.showSeller
      }
      else {
        this.activeSeller = seller, 
        this.showSeller = true
      }
    },
    async createNewSeller() {
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
        component: ModalCreateSellerForm,
        hasModalCard: true,
        trapFocus: true
      })
    }
  },
  async created() {
    await this.$store.dispatch('ca/getSellers')
  },
  computed: {
    sellers() {
      return this.$store.state.ca.sellers
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

.sellers {
  display: grid;
  grid-template-columns: 1fr 1fr;
  margin-left: 0;
}

.sellers-list {
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
    border-radius: 10px;
    border-bottom: 1px solid #f2f2f2;

    &:hover {
      color: #1e6ac8e8;
      background-color: #f2f2f2;
    }
  }
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
</style>
