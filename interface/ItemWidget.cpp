#include "ItemWidget.h"
#include "ui_ItemWidget.h"

ItemWidget::ItemWidget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::ItemWidget)
{
    ui->setupUi(this);
}

ItemWidget::~ItemWidget()
{
    delete ui;
}
