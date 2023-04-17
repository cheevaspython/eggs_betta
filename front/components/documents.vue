<template>
  <form action="" style="width: 900px">
    <div class="modal-card" style="width: 800px; height: 95vh">
      <header class="modal-card-head" style="background-color: #c3c3c3; text-align: center">
        <p class="modal-card-title" style="color: whitesmoke; font-size: 30px; font-weight: 900">Документы</p>
        <button
          type="button"
          class="delete"
          @click="$emit('close')" />
      </header>

      <section class="modal-card-body is-fullwidth">
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-payment_order_incoming/`, 'Платежное поручение входящее')" 
          class="docs" v-show="payment_order_incoming">
          Платежное поручение входящее
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-payment_order_outcoming/`, 'Платежное поручение исходящее')" 
          class="docs" v-show="payment_order_outcoming">
          Платежное поручение исходящее
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-specification_seller/`, 'Спецификация от продавца')" 
          class="docs" v-show="specification_seller">
          Спецификация от продавца
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-account_to_seller/`, 'Счет на оплату продавцу')" 
          class="docs" v-show="account_to_seller">
          Счет на оплату продавцу
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-specification_buyer/`, 'Спецификация покупателя')" 
          class="docs" v-show="specification_buyer">
          Спецификация покупателя
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-account_to_buyer/`, 'Счет на оплату покупателю')" 
          class="docs" v-show="account_to_buyer">
          Счет на оплату покупателю
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-application_contract_logic/`, 'Договор-заявка на транспорт')" 
          class="docs" v-show="application_contract_logic">
          Договор-заявка на транспорт
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-account_to_logic/`, 'Счет на транспорт')" 
          class="docs" v-show="account_to_logic">
          Счет на транспорт
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-UPD_incoming/`, 'Входящая УПД')" 
          class="docs" v-show="UPD_incoming">
          Входящая УПД
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-account_invoicing_from_seller/`, 'Счет-Фактура от продавца')" 
          class="docs" v-show="account_invoicing_from_seller">
          Счет-Фактура от продавца
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-product_invoice_from_seller/`, 'Товарная накладная от продавца')" 
          class="docs" v-show="product_invoice_from_seller">
          Товарная накладная от продавца
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-UPD_outgoing/`, 'Исходящая УПД')" 
          class="docs" v-show="UPD_outgoing">
          Исходящая УПД
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-account_invoicing_from_buyer/`, 'Счет-Фактура от покупателя')" 
          class="docs" v-show="account_invoicing_from_buyer">
          Счет-Фактура от покупателя
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-product_invoice_from_buyer/`, 'Товарная накладная от покупателя')" 
          class="docs" v-show="product_invoice_from_buyer">
          Товарная накладная от покупателя
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-veterinary_certificate_buyer/`, 'Ветеринарное свидетельсвто от покупателя')" 
          class="docs" v-show="veterinary_certificate_buyer">
          Ветеринарное свидетельсвто от покупателя
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-veterinary_certificate_seller/`, 'Ветеринарное свидетельсвто от продавца')" 
          class="docs" v-show="veterinary_certificate_seller">
          Ветеринарное свидетельсвто от продавца
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-international_deal_CMR/`, 'Международная сделка, ЦМР')" 
          class="docs" v-show="international_deal_CMR">
          Международная сделка, ЦМР
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-international_deal_TTN/`, 'Международная сделка, ТТН')" 
          class="docs" v-show="international_deal_TTN">
          Международная сделка, ТТН
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-UPD_logic/`, 'Транспортная УПД')" 
          class="docs" v-show="UPD_logic">
          Транспортная УПД
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-account_invoicing_logic/`, 'Транспортная счет-фактура')" 
          class="docs" v-show="account_invoicing_logic">
          Транспортная счет-фактура
        </div>
        <div @click="showDoc(`http://93.95.97.249/api/eggs/downloads/deal_docs-${docs.id}-product_invoice_logic/`, 'Транспортная товарная накладная')" 
          class="docs" v-show="product_invoice_logic">
          Транспортная товарная накладная
        </div>
      </section>

      <footer class="modal-card-foot is-justify-content-flex-end">
        <b-button
          label="Закрыть"
          @click="$emit('close')"/>
      </footer>
    </div>
  </form>
</template>
  
<script>
import docViewer from "@/components/docViewer"
export default {
  name: 'documents',
  props: ['docs'],
  data() {
    return {
      payment_order_outcoming: this.docs.payment_order_outcoming,
      payment_order_incoming: this.docs.payment_order_incoming,
      specification_seller: this.docs.specification_seller,
      account_to_seller: this.docs.account_to_seller,
      specification_buyer: this.docs.specification_buyer,
      account_to_buyer: this.docs.account_to_buyer,
      application_contract_logic: this.docs.application_contract_logic,
      account_to_logic: this.docs.account_to_logic,
      UPD_incoming: this.docs.UPD_incoming,
      account_invoicing_from_seller: this.docs.account_invoicing_from_seller,
      product_invoice_from_seller: this.docs.product_invoice_from_seller,
      UPD_outgoing: this.docs.UPD_outgoing,
      account_invoicing_from_buyer: this.docs.account_invoicing_from_buyer,
      product_invoice_from_buyer: this.docs.product_invoice_from_buyer,
      veterinary_certificate_buyer: this.docs.veterinary_certificate_buyer,
      veterinary_certificate_seller: this.docs.veterinary_certificate_seller,
      international_deal_CMR: this.docs.international_deal_CMR,
      international_deal_TTN: this.docs.international_deal_TTN,
      UPD_logic: this.docs.UPD_logic,
      account_invoicing_logic: this.docs.account_invoicing_logic,
      product_invoice_logic: this.docs.product_invoice_logic,
    }
  },
  methods: {
    showDoc(url, title) {
      this.$buefy.modal.open({
        parent: this,
        component: docViewer,
        hasModalCard: true,
        trapFocus: true,
        props:{
            doc: [url, title]
          }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
form {
  font-family: 'Montserrat';
}

.docs {
  border: solid 2px #ebebeb;
  background-color: #fff;
  height: 30px;
  width: 100%;
  text-align: center;
  margin-bottom: 10px;
  border-radius: 10px;
  padding-left: 15px;
  cursor: pointer;

  &:hover {
    background-color: #f5f5f5;
  }
}
</style>
  