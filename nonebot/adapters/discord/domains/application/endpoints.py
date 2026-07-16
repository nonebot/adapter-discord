from typing import TYPE_CHECKING, Annotated, Literal

from nonebot.compat import type_validate_python

from .read import (
    SKU,
    Application,
    ApplicationIntegrationTypeConfiguration,
    ApplicationRoleConnectionMetadata,
    AuthorizationResponse,
    Entitlement,
    InstallParams,
    Subscription,
)
from .types import ApplicationFlag, ApplicationIntegrationType
from .write import EditCurrentApplicationParams
from ..gateway.read import ActivityInstance
from ...api.validation import Range, validate
from ...protocol import UNSET, Missing, MissingOrNullable, SnowflakeType
from ...transport.exchange import (
    REST_EXCHANGE,
    BearerAuth,
    BotAuth,
    EmptyResponse,
    JsonBody,
    JsonResponse,
    JsonValueBody,
    RestCall,
    _bool_query,
)

if TYPE_CHECKING:
    from ...api.handle import AdapterProtocol
    from ...bot import Bot


class ApplicationEndpointMixin:
    async def _api_get_current_application(
        self: "AdapterProtocol",
        bot: "Bot",
    ) -> Application:
        """Get current application.

        see https://discord.com/developers/docs/resources/application#get-current-application
        """

        call = RestCall(
            method="GET",
            url=self.base_url / "applications/@me",
            response=JsonResponse(Application),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_edit_current_application(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        custom_install_url: Missing[str] = UNSET,
        description: Missing[str] = UNSET,
        role_connections_verification_url: Missing[str] = UNSET,
        install_params: Missing[InstallParams] = UNSET,
        integration_types_config: Missing[
            dict[ApplicationIntegrationType, ApplicationIntegrationTypeConfiguration]
        ] = UNSET,
        flags: Missing[ApplicationFlag] = UNSET,
        icon: MissingOrNullable[str] = UNSET,
        cover_image: MissingOrNullable[str] = UNSET,
        interactions_endpoint_url: Missing[str] = UNSET,
        tags: Missing[list[str]] = UNSET,
        event_webhooks_url: Missing[str] = UNSET,
        event_webhooks_status: Missing[int] = UNSET,
        event_webhooks_types: Missing[list[str]] = UNSET,
    ) -> Application:
        """Edit current application.

        see https://discord.com/developers/docs/resources/application#edit-current-application
        """

        data = type_validate_python(
            EditCurrentApplicationParams,
            {
                "custom_install_url": custom_install_url,
                "description": description,
                "role_connections_verification_url": role_connections_verification_url,
                "install_params": install_params,
                "integration_types_config": integration_types_config,
                "flags": flags,
                "icon": icon,
                "cover_image": cover_image,
                "interactions_endpoint_url": interactions_endpoint_url,
                "tags": tags,
                "event_webhooks_url": event_webhooks_url,
                "event_webhooks_status": event_webhooks_status,
                "event_webhooks_types": event_webhooks_types,
            },
        )
        call = RestCall(
            method="PATCH",
            url=self.base_url / "applications/@me",
            response=JsonResponse(Application),
            auth=BotAuth(bot.bot_info),
            body=JsonBody(data, omit_unset_values=True),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_application_activity_instance(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        instance_id: str,
    ) -> ActivityInstance:
        """Get application activity instance.

        see https://discord.com/developers/docs/resources/application#get-application-activity-instance
        """

        call = RestCall(
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/activity-instances/{instance_id}",
            response=JsonResponse(ActivityInstance),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_application_role_connection_metadata_records(
        self: "AdapterProtocol", bot: "Bot", *, application_id: SnowflakeType
    ) -> list[ApplicationRoleConnectionMetadata]:
        """Get application role connection metadata records.

        see https://discord.com/developers/docs/resources/application-role-connection-metadata#get-application-role-connection-metadata-records
        """

        call = RestCall(
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/role-connections/metadata",
            response=JsonResponse(list[ApplicationRoleConnectionMetadata]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    @validate
    async def _api_update_application_role_connection_metadata_records(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        records: Annotated[
            list[ApplicationRoleConnectionMetadata],
            Range(message="metadata records must be 0-5 items", max_length=5),
        ],
    ) -> list[ApplicationRoleConnectionMetadata]:
        """Update application role connection metadata records.

        see https://discord.com/developers/docs/resources/application-role-connection-metadata#update-application-role-connection-metadata-records
        """

        payload = [
            type_validate_python(ApplicationRoleConnectionMetadata, record)
            for record in records
        ]
        call = RestCall(
            method="PUT",
            url=self.base_url
            / f"applications/{application_id}/role-connections/metadata",
            response=JsonResponse(list[ApplicationRoleConnectionMetadata]),
            auth=BotAuth(bot.bot_info),
            body=JsonValueBody(payload),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_list_entitlements(  # noqa: PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        user_id: SnowflakeType | None = None,
        sku_ids: tuple[SnowflakeType] | None = None,
        before: SnowflakeType | None = None,
        after: SnowflakeType | None = None,
        limit: int | None = None,
        guild_id: SnowflakeType | None = None,
        exclude_ended: bool | None = None,
        exclude_deleted: bool | None = None,
    ) -> list[Entitlement]:
        """List entitlements.

        see https://discord.com/developers/docs/resources/entitlement#list-entitlements
        """

        params = {
            "user_id": user_id,
            "sku_ids": ",".join(str(sku_id) for sku_id in sku_ids) if sku_ids else None,
            "before": before,
            "after": after,
            "limit": limit,
            "guild_id": guild_id,
            "exclude_ended": _bool_query(value=exclude_ended),
            "exclude_deleted": _bool_query(value=exclude_deleted),
        }
        call = RestCall(
            method="GET",
            url=self.base_url / f"applications/{application_id}/entitlements",
            response=JsonResponse(list[Entitlement]),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_entitlement(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        entitlement_id: SnowflakeType,
    ) -> Entitlement:
        """Get entitlement.

        see https://discord.com/developers/docs/resources/entitlement#get-entitlement
        """

        call = RestCall(
            method="GET",
            url=self.base_url
            / f"applications/{application_id}/entitlements/{entitlement_id}",
            response=JsonResponse(Entitlement),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_consume_an_entitlement(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        entitlement_id: SnowflakeType,
    ) -> None:
        """Consume an entitlement.

        see https://discord.com/developers/docs/resources/entitlement#consume-an-entitlement
        """

        call = RestCall(
            method="POST",
            url=self.base_url
            / f"applications/{application_id}/entitlements/{entitlement_id}/consume",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_create_test_entitlement(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        sku_id: str,
        owner_id: str,
        owner_type: Literal[1, 2],
    ) -> Entitlement:
        """Create test entitlement.

        see https://discord.com/developers/docs/resources/entitlement#create-test-entitlement
        """
        if owner_type not in (1, 2):
            msg = "owner_type must be 1 or 2"
            raise ValueError(msg)

        data = {
            "sku_id": sku_id,
            "owner_id": owner_id,
            "owner_type": owner_type,
        }
        call = RestCall(
            method="POST",
            url=self.base_url / f"applications/{application_id}/entitlements",
            response=JsonResponse(Entitlement),
            auth=BotAuth(bot.bot_info),
            body=JsonValueBody(data),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_delete_test_entitlement(
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        application_id: SnowflakeType,
        entitlement_id: SnowflakeType,
    ) -> None:
        """Delete test entitlement.

        see https://discord.com/developers/docs/resources/entitlement#delete-test-entitlement
        """

        call = RestCall(
            method="DELETE",
            url=self.base_url
            / f"applications/{application_id}/entitlements/{entitlement_id}",
            response=EmptyResponse(),
            auth=BotAuth(bot.bot_info),
        )
        await REST_EXCHANGE.execute(self, call)

    async def _api_list_SKUs(  # noqa: N802
        self: "AdapterProtocol", bot: "Bot", *, application_id: SnowflakeType
    ) -> list[SKU]:
        """List SKUs.

        see https://discord.com/developers/docs/resources/sku#list-skus
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"applications/{application_id}/skus",
            response=JsonResponse(list[SKU]),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    @validate
    async def _api_list_SKU_subscriptions(  # noqa: N802, PLR0913
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        sku_id: SnowflakeType,
        before: SnowflakeType | None = None,
        after: SnowflakeType | None = None,
        limit: Annotated[
            int | None,
            Range(message="limit must be between 1 and 100", ge=1, le=100),
        ] = None,
        user_id: SnowflakeType | None = None,
    ) -> list[Subscription]:
        """List SKU subscriptions.

        see https://discord.com/developers/docs/resources/subscription#list-sku-subscriptions
        """
        if user_id is None:
            msg = "user_id is required for bot token queries"
            raise ValueError(msg)

        params = {
            "before": before,
            "after": after,
            "limit": limit,
            "user_id": user_id,
        }
        call = RestCall(
            method="GET",
            url=self.base_url / f"skus/{sku_id}/subscriptions",
            response=JsonResponse(list[Subscription]),
            auth=BotAuth(bot.bot_info),
            query=params,
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_SKU_subscription(  # noqa: N802
        self: "AdapterProtocol",
        bot: "Bot",
        *,
        sku_id: SnowflakeType,
        subscription_id: SnowflakeType,
    ) -> Subscription:
        """Get SKU subscription.

        see https://discord.com/developers/docs/resources/subscription#get-sku-subscription
        """

        call = RestCall(
            method="GET",
            url=self.base_url / f"skus/{sku_id}/subscriptions/{subscription_id}",
            response=JsonResponse(Subscription),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_current_bot_application_information(
        self: "AdapterProtocol", bot: "Bot"
    ) -> Application:
        """Get current bot application information.

        see https://discord.com/developers/docs/topics/oauth2#get-current-bot-application-information
        """

        call = RestCall(
            method="GET",
            url=self.base_url / "oauth2/applications/@me",
            response=JsonResponse(Application),
            auth=BotAuth(bot.bot_info),
        )
        return await REST_EXCHANGE.execute(self, call)

    async def _api_get_current_authorization_information(
        self: "AdapterProtocol",
        *,
        access_token: str,
    ) -> AuthorizationResponse:
        """Get current authorization information.

        see https://discord.com/developers/docs/topics/oauth2#get-current-authorization-information
        """

        call = RestCall(
            method="GET",
            url=self.base_url / "oauth2/@me",
            response=JsonResponse(AuthorizationResponse),
            auth=BearerAuth(access_token),
        )
        return await REST_EXCHANGE.execute(self, call)


__all__ = ["ApplicationEndpointMixin"]
