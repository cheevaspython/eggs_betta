<template>
  <div>
    <div class="card box" style="width: 40vw" v-if="appFromSeller">
      <div style="background-color: #fff; border-radius: 10px;">
        <h4 class="title has-text-centered border-title">{{ `Заявка от продавца №${appFromSeller.id}` }}</h4>
      </div>
      
      <div class="app app__title">Продукция</div>
      <TableEggs :app="appFromSeller"/>
  
      <div class="app app__title">Продавец</div>
      <div class="app__container">
        <div class="app__info ca" @click="showSeller(appFromSeller.seller_card_detail)">
          <div class="app__info-name">Название</div>
          <div class="app__attr">{{ appFromSeller.seller_card_detail.name }}</div>
        </div>
        <div class="app__info">
          <div class="app__info-name">ИНН</div>
          <div>{{ appFromSeller.seller_card_detail.inn }}</div>
        </div>
        <div class="app__info">
          <div class="app__info-name">Тип оплаты</div>
          <div>{{ typeOfPayment }}</div>
        </div>
        <div class="app__info" v-show="!appFromSeller.pre_payment_application">
          <div class="app__info-name">Отсрочка оплаты</div>
          <div>{{ postponementPayToStr }}</div>
        </div>
        <div class="app__info">
          <div class="app__info-name">Адрес погрузки</div>
          <div class="app__attr">{{ appFromSeller.loading_address }}</div>
        </div>
        <div class="app__info">
          <div class="app__info-name">Окно поставки</div>
          <div>{{ `от ${getStrDay(appFromSeller.delivery_window_from)} до ${getStrDay(appFromSeller.delivery_window_until)}` }}</div>
        </div>
        <div class="app__info" v-show="appFromSeller.comment">
          <div class="app__info-name">Комментарий</div>
          <div class="app__attr">{{ appFromSeller.comment }}</div>
        </div>
        <div class="app__info">
          <div class="app__info-name">Автор</div>
          <div>{{ appFromSeller.owner_detail.first_name + ' ' + appFromSeller.owner_detail.last_name }}</div>
        </div>
      </div>

      <div class="card__button-wrapper">
        <b-button type="is-success is-light" @click="changeAppFromSeller" style="margin-right: 5px">Редактировать</b-button>
        <b-button type="is-danger is-light" @click="toggleIsActive" v-show="canDelete()">Удалить</b-button>
      </div>
    </div>
    <div v-show="showSellerCard" style="float: right">
      <SellerInfo :trader-data="currentSeller"/>
    </div>
  </div>
</template>

<script>
import ModalSellerAppEditForm from '@/components/editForms/ModalSellerAppEditForm'
export default {
  name: 'appFromSeller',
  props: ['appFromSeller'],
  components: {
    SellerInfo: () => import("@/components/cards/SellerInfo")
  },
  data() {
    return {
      currentSeller: null,
      showSellerCard: false
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
    async changeAppFromSeller() {
      const appFromSeller = this.appFromSeller
      this.$buefy.modal.open({
        parent: this,
        component: ModalSellerAppEditForm,
        hasModalCard: true,
        trapFocus: true,
        props:{
          applicationFromSeller: appFromSeller
        }
      })
    },
    async toggleIsActive() {
      if (confirm('Подтвердите удаление')) {
        const appSeller = {
          model_id: this.appFromSeller.id,
          model_title: "Заявка от продавца"
        }
        await this.$store.dispatch('eggs/toggleIsActive', appSeller)
        .finally(async () => 
          this.$store.dispatch('bid/getOwnerTasks'),
          this.$store.dispatch('user/getUserNotifications')
        )
        this.$router.push('/')
      }
    },
    showSeller(seller) {
      if (this.currentSeller == seller) {
        this.showSellerCard = !this.showSellerCard
      }
      else {
        this.showSellerCard = true, 
        this.currentSeller = seller
      }
    },
  },
  computed: {
    typeOfPayment() {
      if (this.appFromSeller.pre_payment_application) {
        return 'Предоплата'
      }
      else {
        return 'Постоплата'
      }
    },
    postponementPayToStr() {
      let day
      if (this.appFromSeller.postponement_pay == 1) {
        day = 'день'
      }
      else if (this.appFromSeller.postponement_pay >= 2 && this.appFromSeller.postponement_pay <= 4) {
        day = 'дня'
      }
      else if (this.appFromSeller.postponement_pay > 5) {
        day = 'дней'
      }
      else {
        return 'Отсутсвует'
      }
      const postponement = `${this.appFromSeller.postponement_pay} ${day}`
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
  background-color: #00a2ff15;
  background-color: #099cf115;
}

.trader-info {
  cursor: pointer;
  &:hover {
    background-color: #f5f5f5;
  }
}

.flexbox {
    display: flex;

    &__column {
      flex-direction: column;
      flex-flow: column;
    }
    &__row {
      flex-direction: row;
      flex-flow: row;
      display: inline-flex;
    }
    &__start {
      justify-content: flex-start;
    }
    &__center {
      justify-content: center;
    }
    &__end {
      justify-content: flex-end;
    }
    &__space-between{
      justify-content: space-between;
    }
  }

.app-type {
  font-size: 14px;
  width: 100%;
  text-align: center;
  padding: 0;
  margin-bottom: 0.2vh;
  border: solid 1px #ebebeb;
  border-radius: 20px;

  &__import {
    background-color: #c411dc3f;
  }
  &__pre-payment {
    background-color: #a9680d4f;
  }
  &__post-payment {
    background-color: #9e9e9e45;
  }
}
</style>
