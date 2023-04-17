<template>
  <div>
    <div class="card box" style="width: 40vw" v-if="appFromBuyer">
      <div style="background-color: #fff; border-radius: 10px;">
        <h4 class="title has-text-centered border-title">{{ `Заявка от покупателя №${appFromBuyer.id}` }}</h4>
      </div>

      <div class="app app__title">Продукция</div>
      <TableEggs :app="appFromBuyer"/>
  
      <div class="app app__title">Покупатель</div>
      <div class="app__container">
        <div class="app__info ca" @click="showBuyer(appFromBuyer.buyer_card_detail)">
          <div class="app__info-name">Название</div>
          <div class="app__attr">{{ appFromBuyer.buyer_card_detail.name }}</div>
        </div>
        <div class="app__info">
          <div class="app__info-name">ИНН</div>
          <div>{{ appFromBuyer.buyer_card_detail.inn }}</div>
        </div>
        <div class="app__info">
          <div class="app__info-name">Отсрочка оплаты</div>
          <div>{{ postponementPayToStr }}</div>
        </div>
        <div class="app__info">
          <div class="app__info-name">Адрес погрузки</div>
          <div class="app__attr">{{ appFromBuyer.unloading_address }}</div>
        </div>
        <div class="app__info">
          <div class="app__info-name">Окно поставки</div>
          <div>{{ `от ${getStrDay(appFromBuyer.delivery_window_from)} до ${getStrDay(appFromBuyer.delivery_window_until)}` }}</div>
        </div>
        <div class="app__info" v-show="appFromBuyer.comment">
          <div class="app__info-name">Комментарий</div>
          <div class="app__attr">{{ appFromBuyer.comment }}</div>
        </div>
        <div class="app__info">
          <div class="app__info-name">Автор</div>
          <div>{{ appFromBuyer.owner_detail.first_name + ' ' + appFromBuyer.owner_detail.last_name }}</div>
        </div>
      </div>

      <div class="card__button-wrapper">
        <b-button type="is-success is-light" style="margin-right: 5px" @click="changeAppFromBuyer">Редактировать</b-button>
        <b-button type="is-danger is-light" @click="toggleIsActive" v-show="canDelete()">Удалить</b-button>
      </div>
    </div>
    <div v-show="showBuyerCard" style="float: right">
      <BuyerInfo :trader-data="currentBuyer"/>
    </div>
  </div>
</template>
  
<script>
import ModalBuyerAppEditForm from '@/components/editForms/ModalBuyerAppEditForm'
export default {
  name: 'appFromBuyer',
  props: ['appFromBuyer'],
  components: {
    BuyerInfo: () => import("@/components/cards/BuyerInfo")
  },
  data() {
    return {
      currentBuyer: null,
      showBuyerCard: false,
    }
  },
  methods: {
    canDelete() {
      const acceptedRoles = ['6', '8']
      if (acceptedRoles.includes(this.currentUserRole)) {
        return true
      }
      else {
        return false
      }
    },
    getStrMonth(month) {
      switch (month) {
        case 0:
          return 'января'
        case 1:
          return 'февраля'
        case 2:
          return 'марта'
        case 3:
          return 'апреля'
        case 4:
          return 'мая'
        case 5:
          return 'июня'
        case 6:
          return 'июля'
        case 7:
          return 'августа'
        case 8:
          return 'сентября'
        case 9:
          return 'октября'
        case 10:
          return 'ноября'
        case 11:
          return 'декабря'
      }
    },
    getStrDay(dateStr) {
      const date = Date.parse(dateStr)
      const currentDate = new Date(date)
      return currentDate.getDate() + ' ' + this.getStrMonth(currentDate.getMonth()) + ' ' + currentDate.getFullYear()
    },
    showBuyer(buyer) {
      if (this.currentBuyer == buyer) {
        this.showBuyerCard = !this.showBuyerCard
      }
      else {
        this.showBuyerCard = true, 
        this.currentBuyer = buyer
      }
    },
    async changeAppFromBuyer() {
      const appFromBuyer = this.$store.state.eggs.currentAppFromBuyer
      this.$buefy.modal.open({
        parent: this,
        component: ModalBuyerAppEditForm,
        hasModalCard: true,
        trapFocus: true,
        props:{
          applicationFromBuyer: appFromBuyer
        }
      })
    },
    async toggleIsActive() {
      if (confirm('Подтвердите удаление')) {
        const appBuyer = {
          model_id: this.appFromBuyer.id,
          model_title: "Заявка от покупателя"
        }
        await this.$store.dispatch('eggs/toggleIsActive', appBuyer)
        .finally(async () => 
          this.$store.dispatch('bid/getOwnerTasks'),
          this.$store.dispatch('user/getUserNotifications')
        )
        this.$router.push('/')
      }
    }
  },
  computed: {
    postponementPayToStr() {
      let day
      if (this.appFromBuyer.postponement_pay == 1) {
        day = 'день'
      }
      else if (this.appFromBuyer.postponement_pay >= 2 && this.appFromBuyer.postponement_pay <= 4) {
        day = 'дня'
      }
      else if (this.appFromBuyer.postponement_pay > 5) {
        day = 'дней'
      }
      else {
        return 'Отсутсвует'
      }
      const postponement = `${this.appFromBuyer.postponement_pay} ${day}`
      return postponement
    }
  }
}
</script>

<style lang="scss" scoped>
.card {
  float: left;
  background-color: #f9f9f9;
  width: 100%;

  &__row {
    display: flex;
    justify-content: space-between;
    margin-bottom: .5rem;
    border-bottom: solid #f5f5f5 2px;
  }
  &__info {
    overflow-wrap: break-word;
    max-width: 500px;
    font-weight: 500;
    margin-left: 1rem;
  }
  &__button-wrapper{
    display: flex;
    justify-content: center;
    border-radius: 10px;
    padding: 2px 5px;
    gap: 5px;
    background-color: #fff;
    border: solid 2px #f3f3f3;
  }
}

.app {
  display: flex;

  &__title {
    width: 100%;
    height: 40px;
    font-size: 20px;
    font-weight: 600;
    color: #7b7b7b;
    margin: 0 auto;
    justify-content: center;
    align-items: center;
    border: solid 2px #f3f3f3;
    border-bottom: 0;
    border-radius: 10px;
    background-color: #fff;
  }
  &__container {
    flex-direction: column;
    flex-flow: column;
    justify-content: center;
    align-items: center;
    background-color: #fff;
    border: solid 2px #f3f3f3;
    border-radius: 10px;
    padding: 7px 5px;
    margin-bottom: 5px;
  }
  &__info {
    display: inline-flex;
    flex-flow: row;
    justify-content: space-between;
    height: 28px;
    width: 100%;
    border-bottom: solid 1.5px #f3f3f3;
    border-radius: 5px;
    padding: 0 10px;
    margin-bottom: 5px;
  }
  &__info-name {
    color: #c4c4c4;
  }
  &__attr {
    display: inline;
    overflow-y: scroll;
    height: 28px;
  }
}

.ca {
  &:hover {
    cursor: pointer;
    color: #1e6ac8e8;
  }
}

.border {
  height: 40px;
  padding-top: 7px;
  border: solid #f8f8f8 2px;
  margin-bottom: 15px;
  border-radius: 5px;
  background-color: #f5f5f5;
}

.border-title {
  height: 40px;
  padding-top: 7px;
  border: solid 2px #f3f3f3;
  border-radius: 5px;
  background-color: #48ff0015;
  background-color: #4ce21115;
}

.trader-info {
  cursor: pointer;
  &:hover {
    background-color: #f5f5f5;
  }
}
</style>
  