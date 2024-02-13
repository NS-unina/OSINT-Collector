import { useEffect, useState } from "react";
import { Launch } from "../types";
import axios from "axios";
import SelectLaunch from "./SelectLaunch";
import ShowResults from "./ShowResults";
import { instaloader, snscrape } from "../types/results";
import TelegramChannelList from "./TelegramChannelList";
import SnscrapeResults from "./SnscrapeResults";
import InstaloaderResults from "./InstaloaderResults";
import InstagramAccountList from "./InstagramAccountList";

const Results = () => {
  const [launches, setLaunches] = useState<Launch[]>([]);
  const [telegramChannels, setTelegramChannels] = useState<snscrape[]>([]);
  const [instagramAccounts, setInstagramAccounts] = useState<instaloader[]>([]);
  const [selectedLaunch, setSelectedLaunch] = useState<Launch | null>(null);
  const [selectedChannel, setSelectedChannel] = useState<snscrape | null>(null);
  const [selectedInstagramAccount, setSelectedInstagramAccount] =
    useState<instaloader | null>(null);
  const [selectedComponent, setSelectedComponent] =
    useState<string>("Launches");

  useEffect(() => {
    fetchLaunches();
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

  const handleComponentChange = (component: string) => {
    setSelectedComponent(component);
    if (component === "Instagram" && !instagramAccounts.length) {
      fetchInstagramAccounts();
    }
    if (component === "Telegram" && !telegramChannels.length) {
      fetchTelegramChannels();
    }

    if (component === "Launches") {
      setSelectedChannel(null);
      setSelectedInstagramAccount(null);
    } else if (component === "Telegram") {
      setSelectedInstagramAccount(null);
      setSelectedLaunch(null);
    } else if (component === "Instagram") {
      setSelectedChannel(null);
      setSelectedLaunch(null);
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
            onClick={() => handleComponentChange("Launches")}
          >
            Launches
          </button>
          <button
            className={`btn mx-2 ${
              selectedComponent === "Telegram"
                ? "btn-success"
                : "btn-outline-success"
            }`}
            onClick={() => handleComponentChange("Telegram")}
          >
            Telegram
          </button>
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
              <ShowResults selectedLaunch={selectedLaunch} />
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
          {selectedChannel != null && (
            <SnscrapeResults results={selectedChannel} />
          )}
          {selectedInstagramAccount != null && (
            <InstaloaderResults results={selectedInstagramAccount} />
          )}
        </div>
      </div>
    </div>
  );
};

export default Results;
