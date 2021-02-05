Description of parameters.
~~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
    :align: center
    :header-rows: 1
    :widths: 5 5

    * - Feature
      - Description
    * - customer
      - age
    * - CardHolder
      - customer id
    * - cheque_count_12m_g*
      - number of customer receipts collected within last 12 months
        before campaign. g* is a product group
    * - cheque_count_3m_g*
      - number of customer receipts collected within last 3 months
        before campaign. g* is a product group
    * - cheque_count_6m_g*	                
      - number of customer receipts collected within last 6 months
        before campaign. g* is a product group
    * - children
      - number of children
    * - crazy_purchases_cheque_count_12m
      - number of customer receipts with items purchased on "crazy"
        marketing campaign collected within last 12 months before campaign
    * - crazy_purchases_cheque_count_1m
      - number of customer receipts with items purchased on "crazy"
        marketing campaign collected within last 1 month before campaign
    * - crazy_purchases_cheque_count_3m
      - number of customer receipts with items purchased on "crazy"
        marketing campaign collected within last 3 months before campaign
    * - crazy_purchases_cheque_count_6m
      - number of customer receipts with items purchased on "crazy"
        marketing campaign collected within last 6 months before campaign
    * - crazy_purchases_goods_count_12m
      - items amount purchased on "crazy" marketing campaign collected
        within last 12 months before campaign
    * - crazy_purchases_goods_count_6m
      - items amount purchased on "crazy" marketing campaign collected
        within last 6 months before campaign
    * - disc_sum_6m_g34
      - discount sum for past 6 month on a 34 product group
    * - food_share_15d
      - food share in customer purchases for 15 days
    * - food_share_1m
      - food share in customer purchases for 1 month
    * - gender
      - customer gender
    * - group
      - treatment/control group flag
    * - k_var_cheque_15d
      - average check coefficient of variation for 15 days
    * - k_var_cheque_3m
      - average check coefficient of variation for 3 months
    * - k_var_cheque_category_width_15d
      - coefficient of variation of the average number of purchased
        categories (2nd level of the hierarchy) in one receipt for 15 days
    * - k_var_cheque_group_width_15d
      - coefficient of variation of the average number of purchased
        groups (1st level of the hierarchy) in one receipt for 15 days
    * - k_var_count_per_cheque_15d_g*
      - unique product id (SKU) coefficient of variation for 15 days
        for g* product group
    * - k_var_count_per_cheque_1m_g*
      - unique product id (SKU) coefficient of variation for 1 month
        for g* product group
    * - k_var_count_per_cheque_3m_g*
      - unique product id (SKU) coefficient of variation for 3 months
        for g* product group
    * - k_var_count_per_cheque_6m_g*
      - unique product id (SKU) coefficient of variation for 6 months
        for g* product group
    * - k_var_days_between_visits_15d
      - coefficient of variation of the average period between visits
        for 15 days
    * - k_var_days_between_visits_1m
      - coefficient of variation of the average period between visits
        for 1 month
    * - k_var_days_between_visits_3m
      - coefficient of variation of the average period between visits
        for 3 months
    * - k_var_disc_per_cheque_15d
      - discount sum coefficient of variation for 15 days
    * - k_var_disc_share_12m_g32
      - discount amount coefficient of variation for 12 months
        for g* product group
    * - k_var_disc_share_15d_g*
      - discount amount coefficient of variation for 15 days
        for g* product group
    * - k_var_disc_share_1m_g*
      - discount amount coefficient of variation for 1 month
        for g* product group
    * - k_var_disc_share_3m_g*
      - discount amount coefficient of variation for 3 months
        for g* product group
    * - k_var_disc_share_6m_g*
      - discount amount coefficient of variation for 6 months
        for g* product group
    * - k_var_discount_depth_15d
      - discount amount coefficient of variation for 1 month
    * - k_var_discount_depth_1m
      - discount amount coefficient of variation for 15 days
    * - k_var_sku_per_cheque_15d
      - number of unique product ids (SKU) coefficient of variation
        for 15 days
    * - k_var_sku_price_12m_g*
      - price coefficient of variation for 15 days, 3, 6, 12 months
        for g* product group
    * - main_format
      - store type (1 - grociery store, 0 - superstore)
    * - mean_discount_depth_15d
      - mean discount depth for 15 days
    * - months_from_register
      - number of months from a moment of register
    * - perdelta_days_between_visits_15_30d
      - timdelta in percent between visits during the first half
        of the month and visits during second half of the month
    * - promo_share_15d
      - promo goods share in the customer bucket
    * - response_att
      - binary target variable = store visit
    * - response_sms
      - share of customer responses to previous SMS.
        Response = store visit
    * - response_viber
      - share of responses to previous Viber messages.
        Response = store visit
    * - sale_count_12m_g*
      - number of purchased items from the group * for 12 months
    * - sale_count_3m_g*
      - number of purchased items from the group * for 3 months
    * - sale_count_6m_g*
      - number of purchased items from the group * for 6 months
    * - sale_sum_12m_g*
      - sum of sales from the group * for 12 months
    * - sale_sum_3m_g*
      - sum of sales from the group * for 3 months
    * - sale_sum_6m_g*
      - sum of sales from the group * for 6 months
    * - stdev_days_between_visits_15d
      - coefficient of variation of the days between visits for 15 days
    * - stdev_discount_depth_15d
      - discount sum coefficient of variation for 15 days
    * - stdev_discount_depth_1m
      - discount sum coefficient of variation for 1 month