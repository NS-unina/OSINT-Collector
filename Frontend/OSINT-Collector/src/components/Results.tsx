import { useEffect, useState } from "react";
import { Launch } from "../types";
import axios from "axios";
import SelectLaunch from "./SelectLaunch";
import ShowResults from "./ShowResults";
import {
  TelegramGroup,
  TelegramMessage,
  blackbird,
  instaloader,
  snscrape,
} from "../types/results";
import TelegramChannelList from "./TelegramChannelList";
import SnscrapeResults from "./SnscrapeResults";
import InstaloaderResults from "./InstaloaderResults";
import InstagramAccountList from "./InstagramAccountList";
import UsernameList from "./UsernameList"; // Aggiunto UsernameList
import BlackbirdResults from "./BlackbirdResults";
import TelegramGroupList from "./TelegramGroupList";
import TelegramTrackerResults from "./TelegramTrackerResults";

const Results = () => {
  const [launches, setLaunches] = useState<Launch[]>([]);
  const [telegramChannels, setTelegramChannels] = useState<snscrape[]>([]);
  const [instagramAccounts, setInstagramAccounts] = useState<instaloader[]>([]);
  const [usernames, setUsernames] = useState<blackbird[]>([]);
  const [telegramGroups, setTelegramGroups] = useState<TelegramGroup[]>([]);
  const [telegramMessages, setTelegramMessages] = useState<TelegramMessage[]>(
    []
  );
  const [selectedLaunch, setSelectedLaunch] = useState<Launch | null>(null);
  const [selectedChannel, setSelectedChannel] = useState<snscrape | null>(null);
  const [selectedInstagramAccount, setSelectedInstagramAccount] =
    useState<instaloader | null>(null);
  const [selectedUsername, setSelectedUsername] = useState<blackbird | null>(
    null
  );
  const [selectedGroup, setSelectedGroup] = useState<TelegramGroup | null>(
    null
  );
  const [selectedComponent, setSelectedComponent] = useState<string>("");

  useEffect(() => {
    fetchLaunches();
    fetchTelegramChannels();
    fetchInstagramAccounts();
    fetchUsernames();
    fetchGroups();
  }, []);

  const fetchLaunches = () => {
    axios
      .get<Launch[]>(`http://localhost:8080/launches`)
      .then((res) => setLaunches(res.data))
      .catch((error) => console.error("Error fetching data:", error));
  };

  const fetchTelegramChannels = () => {
    axios
      .get<snscrape[]>(`http://localhost:8080/telegram/channels`)
      .then((res) => setTelegramChannels(res.data))
      .catch((error) => console.error("Error fetching data:", error));
  };

  const fetchInstagramAccounts = () => {
    axios
      .get<instaloader[]>(`http://localhost:8080/instagram/accounts`)
      .then((res) => setInstagramAccounts(res.data))
      .catch((error) => console.error("Error fetching data:", error));
  };

  const fetchUsernames = () => {
    axios
      .get<blackbird[]>(`http://localhost:8080/usernames`)
      .then((res) => setUsernames(res.data))
      .catch((error) => console.error("Error fetching data:", error));
  };

  const fetchGroups = () => {
    axios
      .get<TelegramGroup[]>(`http://localhost:8080/telegram/groups`)
      .then((res) => setTelegramGroups(res.data))
      .catch((error) => console.error("Error fetching data:", error));
  };

  const fetchTelegramMessages = (peerId: string) => {
    axios
      .get<TelegramMessage[]>(
        `http://localhost:8080/telegram/messages?id=${peerId}`
      )
      .then((res) => setTelegramMessages(res.data))
      .catch((error) => console.error("Error fetching data:", error));
  };

  const moderateTelegramMessages = (peerId: string) => {
    axios
      .get<TelegramMessage[]>(
        `http://localhost:8080/telegram/moderate?id=${peerId}`
      )
      .then(() => fetchTelegramMessages(peerId))
      .catch((error) => console.error("Error fetching data:", error));
  };

  const handleInstaRef = (username: string) => {
    setSelectedComponent("Instagram");
    setSelectedUsername(null);

    const selected = instagramAccounts.find(
      (account) => account.username === username
    );
    if (selected) {
      setSelectedInstagramAccount(selected);
    }
  };

  const handleLaunchToggle = (launchId: number) => {
    const selected = launches.find((l) => l.id === launchId);

    if (selectedLaunch && selectedLaunch.id === launchId) {
      setSelectedLaunch(null);
    } else if (selected) {
      setSelectedLaunch(selected);
    }
  };

  const handleChannelToggle = (channelName: string) => {
    const selected = telegramChannels.find((t) => t.name === channelName);

    if (selectedChannel && selectedChannel.name === channelName) {
      setSelectedChannel(null);
    } else if (selected) {
      setSelectedChannel(selected);
    }
  };

  const handleInstagramAccountToggle = (accountId: string) => {
    const selected = instagramAccounts.find((i) => i.id === accountId);

    if (selectedInstagramAccount && selectedInstagramAccount.id === accountId) {
      setSelectedInstagramAccount(null);
    } else if (selected) {
      setSelectedInstagramAccount(selected);
    }
  };

  const handleUsernameToggle = (username: string) => {
    const selected = usernames.find((u) => u.username === username);

    if (selectedUsername && selectedUsername.username === username) {
      setSelectedUsername(null);
    } else if (selected) {
      setSelectedUsername(selected);
    }
  };

  const handleGroupToggle = (groupId: string) => {
    const selected = telegramGroups.find((g) => g.id === groupId);

    if (selectedGroup && selectedGroup.id === groupId) {
      setSelectedGroup(null);
    } else if (selected) {
      setSelectedGroup(selected);
      setTelegramMessages([]);
      moderateTelegramMessages(selected.id);
    }
  };

  const handleComponentChange = (component: string) => {
    setSelectedComponent(component);
    // if (component === "Instagram" && !instagramAccounts.length) {
    //   fetchInstagramAccounts();
    // }
    // if (component === "Telegram" && !telegramChannels.length) {
    //   fetchTelegramChannels();
    // }
    // if (component === "Usernames" && !usernames.length) {
    //   fetchUsernames();
    // }

    if (component === "Launches") {
      setSelectedChannel(null);
      setSelectedInstagramAccount(null);
      setSelectedUsername(null);
      setSelectedGroup(null);
    } else if (component === "Telegram") {
      setSelectedInstagramAccount(null);
      setSelectedLaunch(null);
      setSelectedUsername(null);
      setSelectedGroup(null);
    } else if (component === "Instagram") {
      setSelectedChannel(null);
      setSelectedLaunch(null);
      setSelectedUsername(null);
      setSelectedGroup(null);
    } else if (component === "Usernames") {
      setSelectedChannel(null);
      setSelectedLaunch(null);
      setSelectedInstagramAccount(null);
      setSelectedGroup(null);
    } else if (component === "TelegramGroups") {
      setSelectedLaunch(null);
      setSelectedChannel(null);
      setSelectedInstagramAccount(null);
      setSelectedUsername(null);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row">
        <div className="col">
          <button
            className={`btn mx-2 ${
              selectedComponent === "Launches"
                ? "btn-success"
                : "btn-outline-success"
            }`}
            style={{ display: "none" }}
            onClick={() => handleComponentChange("Launches")}
          >
            Launches
          </button>
          <div
            className="btn-group-vertical me-2"
            role="group"
            aria-label="Vertical button group"
          >
            <button
              className={`btn ${
                selectedComponent === "Telegram"
                  ? "btn-success"
                  : "btn-outline-success"
              }`}
              onClick={() => handleComponentChange("Telegram")}
            >
              Telegram Channels
            </button>
            <button
              className={`btn ${
                selectedComponent === "TelegramGroups"
                  ? "btn-success"
                  : "btn-outline-success"
              }`}
              onClick={() => handleComponentChange("TelegramGroups")}
            >
              Telegram Groups
            </button>
          </div>
          <button
            className={`btn mx-2 ${
              selectedComponent === "Instagram"
                ? "btn-success"
                : "btn-outline-success"
            }`}
            onClick={() => handleComponentChange("Instagram")}
          >
            Instagram
          </button>
          <button
            className={`btn mx-2 ${
              selectedComponent === "Usernames"
                ? "btn-success"
                : "btn-outline-success"
            }`}
            onClick={() => handleComponentChange("Usernames")}
          >
            Usernames
          </button>
        </div>
      </div>
      <div className="row mt-4">
        <div className="col">
          {selectedComponent === "Launches" && (
            <>
              <SelectLaunch
                launches={!selectedLaunch ? launches : [selectedLaunch]}
                selectedLaunch={selectedLaunch}
                handleLaunchToggle={handleLaunchToggle}
              />
              <ShowResults
                selectedLaunch={selectedLaunch}
                instaRef={handleInstaRef}
              />
            </>
          )}
          {selectedComponent === "Telegram" && (
            <TelegramChannelList
              accounts={!selectedChannel ? telegramChannels : [selectedChannel]}
              selectedChannel={selectedChannel}
              handleChannelToggle={handleChannelToggle}
            />
          )}
          {selectedComponent === "Instagram" && (
            <InstagramAccountList
              accounts={
                !selectedInstagramAccount
                  ? instagramAccounts
                  : [selectedInstagramAccount]
              }
              selectedAccount={selectedInstagramAccount}
              handleAccountToggle={handleInstagramAccountToggle}
            />
          )}
          {selectedComponent === "Usernames" && (
            <UsernameList
              usernames={!selectedUsername ? usernames : [selectedUsername]}
              selectedUsername={selectedUsername}
              handleUsernameToggle={handleUsernameToggle}
            />
          )}
          {selectedComponent === "TelegramGroups" && (
            <TelegramGroupList
              groups={telegramGroups}
              selectedGroup={selectedGroup}
              handleGroupToggle={handleGroupToggle}
            />
          )}
          {selectedChannel != null && (
            <SnscrapeResults results={selectedChannel} />
          )}
          {selectedGroup != null &&
            selectedGroup.messages &&
            (telegramMessages.length > 0 ? (
              <TelegramTrackerResults
                results={telegramMessages}
                channelUsername={selectedGroup.username}
              />
            ) : (
              <TelegramTrackerResults
                results={selectedGroup.messages}
                channelUsername={selectedGroup.username}
              />
            ))}
          {selectedInstagramAccount != null && (
            <InstaloaderResults results={selectedInstagramAccount} />
          )}
          {selectedUsername != null && (
            <BlackbirdResults
              results={selectedUsername}
              instaRef={handleInstaRef}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default Results;
